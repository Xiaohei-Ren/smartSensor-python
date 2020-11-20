# coding: utf-8
# Author：renyuke
# Date ：2020/11/18 10:53
from random import random

from influxdb import InfluxDBClient
import socket


def con_DB(host, pot, user, password, Db):
    """
    连接influxDb
    :param host: localhost
    :param pot: 8086
    :param user:
    :param password:
    :param Db: 数据库名
    :return: InfluxClient
    """
    InfluxClient = InfluxDBClient(host, pot, user, password, Db)
    clientList = InfluxClient.get_list_database()
    print("connect success!")
    print(clientList)
    return InfluxClient


def DB_Insert(InfluxClient, host, id, temp, query):
    """
    插入数据
    :param InfluxClient:
    :param id:
    :param temp:温度
    :param query:select语句
    :return:
    """
    # json形式写入
    tempJson = [{
        "measurement": 'test',
        "tags": {
            'host': host,
        },
        "fields": {
            'id': id,
            'temp': temp,
        }
    }]
    InfluxClient.write_points(tempJson)
    result = InfluxClient.query(query)
    print("Result: {0}".format(result))


conn = con_DB('121.196.147.234', 8086, 'root', '123456', 'test')
InfluxDBClient.get_list_database(conn)
data = 10
hostname = socket.gethostname()
# 获取本机IP
ip = socket.gethostbyname(hostname)

DB_Insert(conn, ip, 1, data, 'select * from test;')
