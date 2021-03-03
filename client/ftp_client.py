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
import os
import json
import hashlib
import sys

from socket import socket

class FtpClient(object):
    def __init__(self, client: socket):
        self.client: socket = client
        self.token: bytes = b'no token'   # current token

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
        """view current dir message."""
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

    def pwd(self, command: str):
        """view current work dir."""
        self.client.send(command.encode())
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        if recv_data['code'] != '000':
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')
            return

        self.client.send(self.token)
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        if recv_data['code'] == '200':
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}, pwd_dir:\n{recv_data["pwd_dir"]}')
        else:
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')

    def get(self, command: str):
        """download file."""
        self.client.send(command.encode())
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        if recv_data['code'] != '000':
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')
            return

        self.client.send(self.token)
        recv_data: dict = json.loads(self.client.recv(1024).decode())
        if recv_data['code'] != '000':
            print(f'code: {recv_data["code"]}, message: {recv_data["message"]}')
            return

        file = command.split()[1]
        total_filesize = recv_data['total_filesize']
        received_filesize = 0
        if os.path.isfile(file):
            received_filesize = os.stat(file).st_size
        if received_filesize >= total_filesize:
            print('File already download completed.')
            self.client.send('405'.encode())
            return
        self.client.send(str(received_filesize).encode())

        m = hashlib.md5()
        f = open(file, 'wb')
        f.seek(received_filesize)
        print('start downloading...')

        while received_filesize < total_filesize:
            last_size = total_filesize - received_filesize
            recv_size = 1024
            if last_size < 1024:
                recv_size = last_size   # avoid sticking the packet.
            data = self.client.recv(recv_size)
            m.update(data)
            f.write(data)
            received_filesize += len(data)
            self.progress_bar(received_filesize=received_filesize, total_filesize=total_filesize, mode='Downloading')

        md5 = m.hexdigest()
        recv_md5 = self.client.recv(1024).decode()
        if recv_md5 == md5:
            print('\nFile download completed.')
        else:
            print('\nMd5 is inconsistent.')

    @staticmethod
    def progress_bar(received_filesize: int, total_filesize: int, mode: str):
        width = 50
        percent = received_filesize / total_filesize
        used_num = int(percent * width)
        unuse_num = int(width - used_num)
        percent = percent * 100
        sys.stdout.write(f'{mode}[{used_num * "#"}{unuse_num * " "}]{int(percent)}%\r')
        sys.stdout.flush()
        return