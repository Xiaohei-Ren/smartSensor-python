import json

from django.shortcuts import render
import datetime
import pytz
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from influxdb import InfluxDBClient
import time
from app_sensor_manage.models import Sensor
import random
import pymysql


# Create your views here.todo：可视化图表增加

def con_DB(query):
    """
    influx数据库连接
    :param query:
    :return:
    """
    InfluxClient = InfluxDBClient('121.196.147.234', 8086, 'root', '123456', 'hs_data')
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
    time_local_str = local_dt.strftime(local_format)
    l_time = time.localtime(int(time.mktime(time.strptime(time_local_str, local_format))))
    return time.strftime(local_format, l_time)


def data_reader_all(id):
    """
    获取24h数据
    :param id:
    :return:
    """
    query = 'select "time","id", "value" from hs_data where id=1 AND time>now()-24h;'
    Data = con_DB(query)
    points = Data.get_points()
    time_list = []
    value_list = []
    for item in points:
        time_item = item["time"]
        value_item = item["value"]

        time_str = str(time_item)
        time_local = utc_to_local(time_str)
        time_list = time_list + [time_local]
        value_list = value_list + [value_item]

    return value_list, time_list


def data_reader_all_2(id):
    """
    数据大屏数据获取
    :param id:
    :return:
    """
    query = 'select "time","id", "value" from hs_data where id=1 AND time>now()-2h;'
    Data = con_DB(query)
    points = Data.get_points()
    time_list = []
    value_list = []
    for item in points:
        time_item = item["time"]
        value_item = item["value"]

        time_str = str(time_item)
        time_local = utc_to_local(time_str)
        time_list = time_list + [time_local]
        value_list = value_list + [value_item]

    return value_list, time_list


def data_reader(id):
    """
    influxdb数据读取
    :param id:
    :return:
    """
    if id == 1:
        query = 'select "time","id", "value" from hs_data where id=1 order by time desc limit 1;'
    Data = con_DB(query)
    # print(Data)
    points = Data.get_points()
    time_local = 0
    value_item = 0
    for item in points:
        time_item = item["time"]
        value_item = item["value"]
        time_str = str(time_item)
        time_local = utc_to_local(time_str)
        time_local = time_local[:19]
    return value_item, time_local


def json_return_vl(request):
    """
    json形式返回初始value列表
    :param request:
    :return:
    """
    (value_list, time_list) = data_reader_all(1)
    return JsonResponse(value_list, safe=False)


def json_return_tl(request):
    """
    json形式返回初始time列表
    :param request:
    :return:
    """
    (value_list, time_list) = data_reader_all(1)
    return JsonResponse(time_list, safe=False)


def json_return_vl_2(request):
    """
    json形式返回初始value列表
    :param request:
    :return:
    """
    (value_list, time_list) = data_reader_all_2(1)
    return JsonResponse(value_list, safe=False)


def json_return_tl_2(request):
    """
    json形式返回初始time列表
    :param request:
    :return:
    """
    (value_list, time_list) = data_reader_all_2(1)
    return JsonResponse(time_list, safe=False)


def json_return_v(request):
    """
    json形式返回更新value
    :param request:
    :return:
    """
    (value, time_n) = data_reader(1)
    return JsonResponse(value, safe=False)


def json_return_t(request):
    """
    json形式返回更新time
    :param request:
    :return:
    """
    (value, time_n) = data_reader(1)
    return JsonResponse(time_n, safe=False)


def dashboard(request):
    """
    dashboard主页面
    :param request:
    :return:
    """
    temp_sensor = Sensor.objects.filter(sort='温度传感器').count()
    temp_sensor_online = Sensor.objects.filter(sort='温度传感器', status='online').count()

    pre_sensor = Sensor.objects.filter(sort='压力传感器').count()
    pre_sensor_online = Sensor.objects.filter(sort='压力传感器', status='online').count()

    flow_sensor = Sensor.objects.filter(sort='流量传感器').count()
    flow_sensor_online = Sensor.objects.filter(sort='流量传感器', status='online').count()

    con_sensor = Sensor.objects.filter(sort='浓度传感器').count()
    con_sensor_online = Sensor.objects.filter(sort='浓度传感器', status='online').count()

    time_now = datetime.datetime.now()

    return render(request, "dashboard_2.html", locals())


def pressure_data(request):
    value = 0
    pre_dict = {'p_n': 0, 'p_a': 0, 'p_max': 0, 'p_min': 0, 'alert': 0}
    (value, time_n) = data_reader(1)
    pre_dict = {'p_n': value, 'p_a': 70.1, 'p_max': 0.563, 'p_min': '正常', 'alert': '无'}
    return JsonResponse(pre_dict, safe=False)


def pressure_data_mid(request):
    value = 0
    pre_dict = {'temp_mid': 0, 'pre_mid': 0, 'vol_mid': 0, 'state_mid': 0, 'al_mid': 0}
    (value, time_n) = data_reader(1)
    r_data = random_data()
    r_data = round(r_data, 3)
    pre_dict = {'temp_mid': value, 'pre_mid': 70.1, 'vol_mid': r_data, 'state_mid': '正常', 'al_mid': '无'}
    return JsonResponse(pre_dict, safe=False)


def sensor_temp_chart(request):
    return render(request, 'sensor_temp_chart.html')


def his_data_chart(request):
    return render(request, 'his_data_chart.html')


def visual_dashboard(request):
    return render(request, 'visual_dashboard_screen.html')


def random_data():
    """
    test 随机数
    :return:
    """
    ret = random.uniform(3, 4)
    return ret


def conn_mysql(date):
    """
    从mysql获取历史数据
    :return:
    """
    connect = pymysql.connect(host='rm-bp1y3s613ztw9rrc42o.mysql.rds.aliyuncs.com', user='renyk',
                              password='Renyuke@001018', db='hydrogenation_station_data', charset='utf8')
    cursor = connect.cursor()
    sql = "select * from compressor_system_data where datetime like %s"
    date = date + '%'
    cursor.execute(sql, date)
    a = cursor.fetchall()

    datetime_list = []
    state_a = []
    pressure_in_a = []
    pressure_out_a = []
    temp_out_a = []
    state_b = []
    pressure_in_b = []
    pressure_out_b = []
    temp_out_b = []

    for i in range(len(a)):
        datetime_list.append(str(a[i][0]))
        state_a.append(str(a[i][1]))
        pressure_in_a.append(str(a[i][2]))
        pressure_out_a.append(str(a[i][3]))
        temp_out_a.append(str(a[i][4]))
        state_b.append(str(a[i][5]))
        pressure_in_b.append(str(a[i][6]))
        pressure_out_b.append(str(a[i][7]))
        temp_out_b.append(str(a[i][8]))

    return datetime_list, state_a, pressure_out_a, pressure_in_a, temp_out_a, state_b, pressure_out_b, pressure_in_b, temp_out_b


#
# (datetime_list, state_a, pressure_out_a, pressure_in_a, temp_out_a, state_b, pressure_out_b, pressure_in_b,
#  temp_out_b) = conn_mysql('2020-07-28')
# print(datetime_list)


a = str(datetime.datetime.now())
a = a[:10]
dateTime = a


def his_time(request):

    (datetime_list, state_a, pressure_out_a, pressure_in_a, temp_out_a, state_b, pressure_out_b, pressure_in_b,
     temp_out_b) = conn_mysql(dateTime)
    return JsonResponse(datetime_list, safe=False)


def his_temp(request):
    (datetime_list, state_a, pressure_out_a, pressure_in_a, temp_out_a, state_b, pressure_out_b, pressure_in_b,
     temp_out_b) = conn_mysql(dateTime)
    return JsonResponse(temp_out_a, safe=False)


def his_pre_out(request):
    (datetime_list, state_a, pressure_out_a, pressure_in_a, temp_out_a, state_b, pressure_out_b, pressure_in_b,
     temp_out_b) = conn_mysql(dateTime)
    return JsonResponse(pressure_out_a, safe=False)


def his_pre_in(request):
    (datetime_list, state_a, pressure_out_a, pressure_in_a, temp_out_a, state_b, pressure_out_b, pressure_in_b,
     temp_out_b) = conn_mysql(dateTime)
    return JsonResponse(pressure_in_a, safe=False)


@csrf_exempt
def data_set(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        date = post_data.get("date")
        global dateTime
        dateTime = str(date)
        print(date)
    return HttpResponse('success!')
