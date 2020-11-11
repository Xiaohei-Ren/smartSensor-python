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
