import datetime
from random import randrange

import pytz
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from influxdb import InfluxDBClient
import pandas
import numpy
import pyecharts.options as opts
import time
from rest_framework.views import APIView

# Create your views here.
from pandas.io import json
from pyecharts.charts import Line, Bar
from pyecharts.globals import ThemeType


def con_DB(query):
    """
    influx数据库连接
    :param query:
    :return:
    """
    InfluxClient = InfluxDBClient('localhost', 8086, 'ren', '123456', 'temdb')
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


def data_reader(id):
    """
    influxdb数据读取
    :param id:
    :return:
    """
    if id == 1:
        query = 'select "time","id", "temp" from test where id=1;'
    elif id == 2:
        query = 'select "time","id", "temp" from test where id=2;'
    Data = con_DB(query)
    print(Data)
    points = Data.get_points()
    time_list = []
    value_list = []
    for item in points:
        time_item = item["time"]
        value_item = item["temp"]

        time_str = str(time_item)
        time_local = utc_to_local(time_str)

        # time_local = time_local[10:]
        # time_date = time_str[:10]

        # if time.strftime('%Y-%m-%d') == time_date:
        #     print("Date Match---------->")
        #
        #     time_list = time_list + [time_local]
        #     value_list = value_list + [value_item]
        #
        #     print("Value:", item["value"], "LocalTime:", time_local)
        # else:
        #     print("Cant Match----------X")

        time_list = time_list + [time_local]
        value_list = value_list + [value_item]

        print("Value:", item["temp"], "LocalTime:", time_local)
    print("TimeList: ", time_list)
    print("ValueList:", value_list)
    return time_list, value_list


def temp_line() -> Line:
    """
    折线图绘制
    :return:
    """
    (time_list, value_list) = data_reader(1)
    (time_list1, value_list1) = data_reader(2)
    x_data = time_list
    y_data = value_list
    y_data1 = value_list1

    c = (
        Line(init_opts=opts.InitOpts(
            width="1800px", height="500px", theme=ThemeType.WHITE
        )
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="测试"),
            tooltip_opts=opts.TooltipOpts(is_show=True),
            legend_opts=opts.LegendOpts(is_show=True, selected_mode=False, item_height=17),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=5, color="#9966FF", )
                ),
            ),
            # datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100)],
            toolbox_opts=opts.ToolboxOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name="℃",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=5, color="#9966FF")
                )
            ),

        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="温度传感器TS01",
            y_axis=y_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=3, color="orange"),
            # color="orange",
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1, color="orange"),
        )
            .add_yaxis(
            series_name="温度传感器TS02",
            y_axis=y_data1,
            symbol="emptyCircle",
            is_symbol_show=True,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=3, color="blue"),
            # color="pink",
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1, color="blue"),
        )
            .dump_options_with_quotes()
    )
    return c


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(temp_line()))


cnt = 9


class ChartUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        global cnt
        cnt = cnt + 1
        return JsonResponse({"name": cnt, "value": randrange(0, 100)})


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/index.html").read())
