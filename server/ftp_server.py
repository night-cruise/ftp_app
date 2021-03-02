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

from helpers import hash, generate_json
from settings import USER_DB, BASE_DIR

class MyTcpHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super(MyTcpHandler, self).__init__(*args, **kwargs)
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
        """user register."""
        try:
            command_ls: list = command.split()
            command: str = command_ls[0]
            username: str = command_ls[1]
            password: str = command_ls[2]
        except:
            self.request.send(generate_json('400').encode())
            return

        if command != 'register':
            self.request.send(generate_json('400').encode())
            return

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