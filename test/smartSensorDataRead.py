from influxdb import InfluxDBClient
import time
import random
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


def con_DB(host, pot, user, password, Db, id, temp, query):
    client = InfluxDBClient(host, pot, user, password, Db)
    clientList = client.get_list_database()
    print(clientList)

    # 写入数据库
    second = sleep_time(0, 0, 2)
    while True:
        temJson = [{
            "measurement": 'test',
            "tags": {
                'id': id,
            },
            "fields": {
                'temp': temp,
            }
        }]
        time.sleep(second)
        client.write_points(temJson)
        result = client.query(query)
        print("Result: {0}".format(result))
        temp = random.randint(20, 30)


if __name__ == '__main__':
    temp = random.randint(20, 30)
    con_DB('localhost', 8086, 'ren', '123456', 'temdb', 1, temp, 'select * from test;')

    client_fd = plc_connect('192.168.2.1', 2)
    print("connect success")
    # write_VB(client_fd, 2, "8")
    data = read_VB(client_fd, 2)
    print(data)
    plc_con_close(client_fd)
