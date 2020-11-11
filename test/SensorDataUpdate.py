# coding: utf-8
# Author：renyuke
# Date ：2020/11/11 9:49

import struct
from influxdb import InfluxDBClient
import time
import snap7


def plc_connect(ip, type, rack=0, slot=1):
    """
    连接初始化
    :param ip: plc中固定ip
    :param rack: 通常为0
    :param slot: 根据plc安装，一般为0或1
    :return:client
    """
    client = snap7.client.Client()
    client.set_connection_type(type)
    client.connect(ip, rack, slot)
    return client


def plc_con_close(client):
    """
    连接关闭
    :param client:
    :return:
    """
    client.disconnect()


def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec


def read_VD(offset, count):
    """
    读取VD中数据
    :param offset: plc中起始位 例：VD100，VD200
    :param count: 从起始位开始读取位数 VD数据通常为4位
    :return: VDData
    """
    # 获取PLC中数据所在位VD200-VD204
    offsetData = client_fd.read_area(0x84, 1, offset, count)
    print(offsetData)
    # 数据转换为浮点数1
    VDData = snap7.util.get_real(offsetData, 0)
    print(VDData)
    # 数据转换为浮点数2
    VDData1 = struct.unpack(">f", offsetData)
    print(VDData1[0])
    return VDData


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


def DB_Insert(InfluxClient, id, temp, query):
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
            'id': id,
        },
        "fields": {
            'temp': temp,
        }
    }]
    InfluxClient.write_points(tempJson)
    result = InfluxClient.query(query)
    print("Result: {0}".format(result))


if __name__ == '__main__':
    # 连接plc
    client_fd = plc_connect('192.168.2.1', 2)
    print("connect success")

    # 每5s读取温度数据并写入influxDb
    second = sleep_time(0, 0, 5)
    while True:
        # 从VD200开始读取4位，并转换为浮点数
        data = read_VB(200, 4)
        time.sleep(second)
        # 数据存入influxDB（database：temdb，measurement：test）
        conn = con_DB('localhost', 8086, 'root', '123456', 'temdb')
        DB_Insert(conn, 1, data, 'select * from test;')
