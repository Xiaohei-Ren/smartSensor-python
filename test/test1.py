import datetime

import pytz

from influxdb import InfluxDBClient

import time


# coding: utf-8
# Author：renyuke
# Date ：2020/11/23 10:17


def con_DB(query):
    """
    influx数据库连接
    :param query:
    :return:
    """
    InfluxClient = InfluxDBClient('localhost', 8086, 'root', '123456', 'test')
    clientList = InfluxClient.get_list_database()
    print("----------Connect Success----------")
    print("clientList:", clientList)
    result = InfluxClient.query(query)
    InfluxClient.close()
    return result


def utc_to_local(utc_time_str, local_format="%Y-%m-%d %H:%M:%S", utc_format=f'%Y-%m-%dT%H:%M:%S'):
    """
    utc时间转换
    :param utc_time_str: str格式utc时间
    :param local_format:
    :param utc_format:
    :return: 本地时间
    """
    utc_time_str = utc_time_str[0:19]  # 时间精确到秒级
    local_tz = pytz.timezone('Asia/Shanghai')
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    ltime = time.localtime(int(time.mktime(time.strptime(time_str, local_format))))
    return time.strftime(local_format, ltime)


def reader(Data):
    points = Data.get_points()
    time_list = []
    value_list = []
    for item in points:
        time_item = item["time"]
        value_item = item["value"]

        time_str = str(time_item)
        time_local = utc_to_local(time_str)

        time_local = time_local[10:]

        time_list = time_list + [time_local]
        value_list = value_list + [value_item]

    return time_list, value_list


def data_reader():
    """
    influxdb数据读取
    :param id:
    :return:
    """
    query = 'select "time","id", "value" from sensor01 where id=1;'
    Data = con_DB(query)
    # print(Data)
    (time_list_his, value_list_his) = reader(Data)
    return time_list_his, value_list_his


def data_reader_new():
    """
    influxdb数据读取
    :param id:
    :return:
    """
    query = 'SELECT "time","id", "value" FROM sensor01 GROUP BY * ORDER BY DESC LIMIT 1'
    Data = con_DB(query)
    # print(Data)
    (time_list_new, value_list_new) = reader(Data)
    return time_list_new, value_list_new


(time_list_his, value_list_his) = data_reader()
(time_list_new, value_list_new) = data_reader_new()
print("1:", value_list_new)
print("3:", value_list_his)
time_list = time_list_his + time_list_new
value_list_his.extend(value_list_new)
# print(time_list)
value_list_his.pop(0)
print("2:", value_list_his)
