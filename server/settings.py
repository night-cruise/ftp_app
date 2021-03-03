#!/user/bin/python
# -*-coding:UTF-8-*-
""" 
@Author:    Night Cruising
@File:      settings.py
@Time:      2021/03/02
@Version:   3.7.3
@Desc:      None
"""
# here put the import lib
import os

STATUS_CODE = {
    '000': 'no message.',
    '200': 'Request success.',
    '201': 'Created success.',
    '400': 'Parameter error.',
    '401': 'Auth error, please login again.',
    '402': 'User\dir\file has existed',
    '403': 'No permission.',
    '404': 'Not found.',
    '405': 'File has been completed.'
}

DIST_QUOTA = 1024*1024*100
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + '\home'
TEST_USER_DB = 'test.db'
USER_DB = 'user.db' # dict structure
IP_PORT = ('localhost', 9999)
SECRET_KEY = os.getenv('SECRET_KEY', 'secret key')