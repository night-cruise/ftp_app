#!/user/bin/python
# -*-coding:UTF-8-*-
""" 
@Author:    Night Cruising
@File:      ftp_client.py
@Time:      2021/03/02
@Version:   3.7.3
@Desc:      None
"""
# here put the import lib
import json

from socket import socket

class FtpClient(object):
    def __init__(self, client: socket):
        self.client = client

    def run(self):
        while True:
            command: str = input('input command: ')
            if not command:
                continue
            if command == 'exit':
                break
            command_prefix: str = command.split()[0]
            if hasattr(self, command_prefix):
                func = getattr(self, command_prefix)
                func(command)
            else:
                print('command error.')

    def register(self, command: str):
        """user register."""
        self.client.send(command.encode())
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')