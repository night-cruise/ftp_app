#!/user/bin/python
# -*-coding:UTF-8-*-
""" 
@Author:    Night Cruising
@File:      parse.py
@Time:      2021/03/04
@Version:   3.7.3
@Desc:      None
"""
# here put the import lib
def parse_command(command_name: str, command: str):
    return ParseCommand().parse(command_name=command_name, command=command)

class ParseCommand(object):

    def parse(self, command_name: str, command: str):
        if not hasattr(self, command_name):
            return False
        parse_func = getattr(self, command_name)
        return parse_func(command)

    def register(self, command: str):
        try:
            command_ls: list = command.split()
            command: str = command_ls[0]
            username: str = command_ls[1]
            password: str = command_ls[2]
        except:
            return False
        if command != 'register':
            return False

        return username, password

    def login(self, command: str):
        try:
            command_ls: list = command.split()
            command: str = command_ls[0]
            username: str = command_ls[1]
            password: str = command_ls[2]
        except:
            return False
        if command != 'login':
            return False

        return username, password

    def cd(self, command: str):
        try:
            command_ls: list = command.split()
            command: str = command_ls[0]
            dirname: str = command_ls[1]
        except:
            return False
        if command != 'cd':
            return False

        return dirname

    def mkdir(self, command: str):
        try:
            command_ls: list = command.split()
            command: str = command_ls[0]
            dirname: str = command_ls[1]
        except:
            return False

        if command != 'mkdir':
            return False
        return dirname

    def dir(self, command: str):
        try:
            command_ls: list = command.split()
            command: str = command_ls[0]
        except:
            return False
        if command != 'dir':
            return False

        return True

    def pwd(self, command: str):
        try:
            command_ls: list = command.split()
            command: str = command_ls[0]
        except:
            return False
        if command != 'pwd':
            return False

        return True

    def get(self, command: str):
        try:
            command_ls: list = command.split()
            command: str = command_ls[0]
            filename: str = command_ls[1]
        except:
            return False
        if command != 'get':
            return False

        return filename

    def put(self, command: str):
        try:
            command_ls: list = command.split()
            command: str = command_ls[0]
            filename: str = command_ls[1]
        except:
            return False
        if command != 'put':
            return False

        return filename