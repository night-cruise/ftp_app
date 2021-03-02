#!/user/bin/python
# -*-coding:UTF-8-*-
""" 
@Author:    Night Cruising
@File:      run_server.py
@Time:      2021/03/02
@Version:   3.7.3
@Desc:      None
"""
# here put the import lib
import socketserver
from settings import IP_PORT
from ftp_server import MyTcpHandler

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(IP_PORT, MyTcpHandler)
    server.serve_forever()