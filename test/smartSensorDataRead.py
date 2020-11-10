import struct
from influxdb import InfluxDBClient
import time
import snap7


def plc_connect(ip, type, rack=0, slot=1):
    """
    连接初始化
    :param ip:
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


def read_VB(client, offset):
    """
    :param client: client
    :param offset: int
    :returns: str.
    """
    vb_data = client.db_read(1, offset, 1)
    return vb_data[0]


def write_VB(client, offset, data):
    """
    :param client: client
    :param offset: int
    :param data: str
    """
    data = int(data)
    temp = hex(int(data))[2:]
    if data < 0 or data > 255:
        print("请输入0-255之间的数")
    else:
        if data < 16:
            temp = "0" + temp
        client.db_write(1, offset, bytes.fromhex(temp))
        print("向寄存器VB" + str(offset) + "写入" + str(data) + "成功")


def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec


def con_DbInsert(host, pot, user, password, Db, id, temp, query):
    """
    :param host: localhost
    :param pot: 8086
    :param user:
    :param password:
    :param Db:
    :param id: id
    :param temp: 采集传入温度
    :param query:'select * from test;'
    :return:
    """
    client = InfluxDBClient(host, pot, user, password, Db)
    clientList = client.get_list_database
    print(clientList)

    # 写入数据库
    tempJson = [{
        "measurement": 'test',
        "tags": {
            'id': id,
        },
        "fields": {
            'temp': temp,
        }
    }]
    client.write_points(tempJson)
    result = client.query(query)
    print("Result: {0}".format(result))


if __name__ == '__main__':
    # 访问plc取数据
    client_fd = plc_connect('192.168.2.1', 2)
    print("connect success")

    # 每5s读取温度数据并写入influxDb
    second = sleep_time(0, 0, 5)
    while True:
        # 获取PLC中数据所在位VD200-VD204
        data = client_fd.read_area(0x84, 1, 200, 4)
        print(data)
        # 数据转换为浮点数1
        data1 = snap7.util.get_real(data, 0)
        print(data1)
        # 数据转换为浮点数2
        data2 = struct.unpack(">f", data)
        print("当前温度{}", data2[0])
        time.sleep(second)
        # 数据存入influxDB（database：temdb，measurement：test）
        con_DbInsert('localhost', 8086, 'root', '123456', 'temdb', 1, data1, 'select * from test;')

    plc_con_close(client_fd)
