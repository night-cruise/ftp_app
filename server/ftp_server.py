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
import socketserver

from typing import Optional

from server.helpers import hash, generate_json, generate_token, validate_token, parse_command
from server.settings import USER_DB, BASE_DIR

class MyTcpHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super(MyTcpHandler, self).__init__(*args, **kwargs)
        self.username: Optional[str] = None     # current username
        self.home_dir: Optional[str] = None     # current user dir
        self.user_dir: Optional[str] = None     # current user home dir

    def handle(self) -> None:
        while True:
            try:
                command: str = self.request.recv(1024).decode()
                command_prefix: str = command.split()[0]

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
        user_db[username] = {'username': username, 'password': hashed_password}
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

        self.username = username                    # set current user username
        self.home_dir = f'{BASE_DIR}\{username}'    # set current user homedir
        self.user_dir = self.home_dir               # set current user userdir

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

    def _set_user(self):
        pass

    def _reset_user(self):
        self.home_dir = None
        self.user_dir = None
        self.username = None