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
        self.client: socket = client
        self.token: bytes = b''   # current token

    def run(self):
        while True:
            command: str = input('input command: ').strip()
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
        """register user."""
        self.client.send(command.encode())
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')

    def login(self, command: str):
        """login user."""
        self.client.send(command.encode())
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')

        if recv_data['code'] == '200':
            self.client.send('000'.encode())
            token = self.client.recv(1024)
            self.token = token

    def cd(self, command: str):
        """cd dir."""
        self.client.send(command.encode())
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        if recv_data['code'] != '000':
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')
            return

        self.client.send(self.token)
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')

    def mkdir(self, command: str):
        """make dir."""
        self.client.send(command.encode())
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        if recv_data['code'] != '000':
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')
            return

        self.client.send(self.token)
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')

    def dir(self, command: str):
        """view current dir."""
        self.client.send(command.encode())
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        if recv_data['code'] != '000':
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')
            return

        self.client.send(self.token)
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        if recv_data['code'] == '200':
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}, dir_message:\n{recv_data["dir_message"]}')
        else:
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')