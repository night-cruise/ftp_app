#!/user/bin/python
# -*-coding:UTF-8-*-
""" 
@Author:    Night Cruising
@File:      run_client.py
@Time:      2021/03/02
@Version:   3.7.3
@Desc:      None
"""
# here put the import lib
import socket
from settings import IP_PORT
from ftp_client import FtpClient

client = socket.socket()
client.connect(IP_PORT)

if __name__ == '__main__':
    client = FtpClient(client=client)
    client.run()