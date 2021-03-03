#!/user/bin/python
# -*-coding:UTF-8-*-
""" 
@Author:    Night Cruising
@File:      helpers.py
@Time:      2021/03/02
@Version:   3.7.3
@Desc:      None
"""
# here put the import lib
import json
import hashlib

from settings import STATUS_CODE, SECRET_KEY
from typing import Optional
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def hash(password: str):
    m = hashlib.md5()
    m.update(password.encode())
    return m.hexdigest()

def generate_json(status_code: str, **kwargs):
    data = {'code': status_code, 'message': STATUS_CODE[status_code]}
    data.update(**kwargs)
    return json.dumps(data)


def generate_token(username: str, expire_in: Optional[str] = None):
    s = Serializer(secret_key=SECRET_KEY, expires_in=expire_in)
    data = {'username': username}
    return s.dumps(data)

def validate_token(username: str, token: bytes):
    s = Serializer(secret_key=SECRET_KEY)
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    if not data.get('username'):
        return False

    if username != data.get('username'):
        return False
    return True

def parse_command(command_name: str, command: str):
    if command_name == 'register':
        return parse_register_command(command)
    elif command_name == 'login':
        return parse_login_command(command)
    elif command_name == 'cd':
        return parse_cd_command(command)
    elif command_name == 'mkdir':
        return parse_mkdir_command(command)
    elif command_name == 'dir':
        return parse_dir_command(command)
    elif command_name == 'pwd':
        return parse_pwd_command(command)
    elif command_name == 'get':
        return parse_get_command(command)

def parse_register_command(command: str):
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

def parse_login_command(command: str):
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

def parse_cd_command(command: str):
    try:
        command_ls: list = command.split()
        command: str = command_ls[0]
        dirname: str = command_ls[1]
    except:
        return False

    if command != 'cd':
        return False

    return dirname

def parse_mkdir_command(command: str):
    try:
        command_ls: list = command.split()
        command: str = command_ls[0]
        dirname: str = command_ls[1]
    except:
        return False

    if command != 'mkdir':
        return False

    return dirname

def parse_dir_command(command: str):
    try:
        command_ls: list = command.split()
        command: str = command_ls[0]
    except:
        return False

    if command != 'dir':
        return False

    return True

def parse_pwd_command(command: str):
    try:
        command_ls: list = command.split()
        command: str = command_ls[0]
    except:
        return False

    if command != 'pwd':
        return False

    return True

def parse_get_command(command: str):
    try:
        command_ls: list = command.split()
        command: str = command_ls[0]
        filename: str = command_ls[1]
    except:
        return False

    if command != 'get':
        return False

    return filename