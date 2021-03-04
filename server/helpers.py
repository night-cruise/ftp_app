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