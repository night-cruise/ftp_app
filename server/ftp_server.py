#!/user/bin/python
# -*-coding:UTF-8-*-
""" 
@Author:    Night Cruising
@File:      ftp_server.py
@Time:      2021/03/02
@Version:   3.7.3
@Desc:      None
"""
# here put the import lib
import os
import json
import hashlib
import socketserver

from typing import Optional
from helpers import hash, generate_json, generate_token, validate_token
from parse import parse_command
from settings import USER_DB, BASE_DIR, DISK_QUOTA

class MyTcpHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super(MyTcpHandler, self).__init__(*args, **kwargs)
        self.username: Optional[str] = None     # current username
        self.home_dir: Optional[str] = None     # current user dir
        self.user_dir: Optional[str] = None     # current user home dir
        self.disk_quota: int = 0                # current user disk quota

    def handle(self) -> None:
        while True:
            try:
                command: str = self.request.recv(1024).decode()
                command_prefix: str = command.split()[0] if command else None

                if hasattr(self, command_prefix):
                    func = getattr(self, command_prefix)
                    func(command)
                else:
                    self.request.send(generate_json('400').encode())

            except ConnectionResetError as e:
                print(e)
                break


    def register(self, command: str):
        """register user."""
        command_parse = parse_command(command_name='register', command=command)
        if not command_parse:
            self.request.send(generate_json('400').encode())
            return
        username, password = command_parse

        with open(USER_DB, 'r', encoding='utf-8') as f:
            data = json.load(f)

        user_db: dict = data if data else {}
        if username in user_db:
            self.request.send(generate_json('402').encode())
            return

        hashed_password = hash(password)
        user_db[username] = {'username': username, 'password': hashed_password, 'disk_quota': 0}
        with open(USER_DB, 'w', encoding='utf-8') as f:
            json.dump(user_db, f)

        os.mkdir(f'{BASE_DIR}\{username}')
        self.request.send(generate_json('201').encode())

    def login(self, command: str):
        """login user."""
        command_parse = parse_command(command_name='login', command=command)
        if not command_parse:
            self.request.send(generate_json('400').encode())
            return
        username, password = command_parse

        with open(USER_DB, 'r', encoding='utf-8') as f:
            user_db = json.load(f)

        hashed_password = hash(password)
        if username not in user_db or user_db[username]['password'] != hashed_password:
            self.request.send(generate_json('401').encode())
            return

        self.username = username                             # set current user username
        self.home_dir = f'{BASE_DIR}\{username}'             # set current user homedir
        self.user_dir = self.home_dir                        # set current user userdir
        self.disk_quota = user_db[username]['disk_quota']    # set current user disk quota

        token = generate_token(username=username)
        self.request.send(generate_json('200').encode())
        self.request.recv(1024)     # avoid sticking the packet.
        self.request.send(token)


    def cd(self, command: str):
        """cd dir."""
        command_parse = parse_command(command_name='cd', command=command)
        if not command_parse:
            self.request.send(generate_json('400').encode())
            return
        dirname = command_parse

        if not self._validate_token():
            return

        if dirname == '..':
            if len(self.user_dir) > len(self.home_dir):
                self.user_dir = os.path.dirname(self.user_dir)
                self.request.send(generate_json('200').encode())
            else:
                self.request.send(generate_json('403').encode())
            return
        cd_dir = f'{self.user_dir}\{dirname}'
        if os.path.isdir(cd_dir):
            self.user_dir = cd_dir
            self.request.send(generate_json('200').encode())
        else:
            self.request.send(generate_json('404').encode())

    def mkdir(self, command: str):
        """make dir."""
        command_parse = parse_command(command_name='mkdir', command=command)
        if not command_parse:
            self.request.send(generate_json('400').encode())
            return
        dirname = command_parse

        if not self._validate_token():
            return

        mk_dir = f'{self.user_dir}\{dirname}'
        if os.path.isdir(mk_dir):
            self.request.send(generate_json('402').encode())
            return

        os.mkdir(mk_dir)
        self.request.send(generate_json('200').encode())

    def dir(self, command: str):
        """view current dir message"""
        if not parse_command(command_name='dir', command=command):
            self.request.send(generate_json('400').encode())
            return

        if not self._validate_token():
            return

        dir_message = os.popen(f'dir {self.user_dir}').read()
        return self.request.send(generate_json('200', dir_message=dir_message).encode())

    def pwd(self, command: str):
        """view current work dir."""
        if not parse_command(command_name='pwd', command=command):
            self.request.send(generate_json('400').encode())
            return

        if not self._validate_token():
            return

        self.request.send(generate_json('200', pwd_dir=self.user_dir).encode())

    def get(self, command: str):
        """download file."""
        command_parse = parse_command(command_name='get', command=command)
        if not command_parse:
            self.request.send(generate_json('400').encode())
            return
        filename = command_parse

        if not self._validate_token():
            return

        file = f'{self.user_dir}\{filename}'
        if not os.path.isfile(file):
            self.request.send(generate_json('404').encode())
            return

        total_filesize = os.stat(file).st_size
        self.request.send(generate_json('000', total_filesize=total_filesize).encode())
        recv_data = self.request.recv(1024).decode()
        if recv_data == '405':
            return
        received_filesize = int(recv_data)

        m = hashlib.md5()
        f = open(file, 'rb')
        f.seek(received_filesize)

        for line in f:
            m.update(line)
            self.request.send(line)

        self.request.send(m.hexdigest().encode())

    def put(self, command: str):
        """upload file."""
        command_parse = parse_command(command_name='put', command=command)
        if not command_parse:
            self.request.send(generate_json('400').encode())
            return
        filename = command_parse

        if not self._validate_token():
            return

        file = f'{self.user_dir}\{filename}'
        received_filesize = 0
        if os.path.isfile(file):
            received_filesize = os.stat(file).st_size
        self.request.send(generate_json('000', received_filesize=received_filesize).encode())

        recv_data = self.request.recv(1024).decode()
        if recv_data == '405':
            return
        total_filesize = int(recv_data)

        need_disk = total_filesize - received_filesize
        if (self.disk_quota + need_disk) > DISK_QUOTA:
            self.request.send(generate_json('407').encode())
            return
        else:
            self.request.send(generate_json('000').encode())

        self.request.recv(1024)     # avoid sticking the packet.

        m = hashlib.md5()
        f = open(file, 'wb')
        f.seek(received_filesize)

        while received_filesize < total_filesize:
            last_size = total_filesize - received_filesize
            recv_size = 1024
            if last_size < 1024:
                recv_size = last_size   # avoid sticking the packet.
            data = self.request.recv(recv_size)
            m.update(data)
            f.write(data)
            received_filesize += len(data)

        self.disk_quota += need_disk
        with open(USER_DB, 'r', encoding='utf-8') as f:
            user_db = json.load(f)
        user_db[self.username]['disk_quota'] = self.disk_quota
        with open(USER_DB, 'w', encoding='utf-8') as f:
            json.dump(user_db, f)

        self.request.send(m.hexdigest().encode())


    def _validate_token(self):
        self.request.send(generate_json('000').encode())  # avoid sticking the packet.
        token = self.request.recv(1024)

        if not hasattr(self, 'username'):
            self.request.send(generate_json('401').encode())
            return False

        if not validate_token(self.username, token):
            self._reset_user()
            self.request.send(generate_json('401').encode())
            return False
        return True

    def _reset_user(self):
        self.home_dir = None
        self.user_dir = None
        self.username = None