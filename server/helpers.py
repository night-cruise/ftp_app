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
import hashlib
import json
from settings import STATUS_CODE

def hash(password: str):
    m = hashlib.md5()
    m.update(password.encode())
    return m.hexdigest()

def generate_json(status_code: str):
    return json.dumps({'code': status_code, 'message': STATUS_CODE[status_code]})