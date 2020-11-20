import datetime

import pytz
from django.shortcuts import render
from django.http import HttpResponse
from influxdb import InfluxDBClient
import pandas
import numpy
import pyecharts.options as opts
import time

# Create your views here.
from pyecharts.charts import Line, Bar
from pyecharts.globals import ThemeType


def con_DB(query):
    InfluxClient = InfluxDBClient('localhost', 8086, 'ren', '123456', 'temdb')
    clientList = InfluxClient.get_list_database()
    print("----------Connect Success----------")
    print("clientList:", clientList)
    result = InfluxClient.query(query)
    return result


def utc_to_local(utc_time_str, local_format="%Y-%m-%d %H:%M:%S", utc_format=f'%Y-%m-%dT%H:%M:%S'):
    """

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


def index(request):
    if id == 1:
        query = 'select "time","id", "value" from temp where id=1;'
    Data = con_DB(query)
    print(Data)
    points = Data.get_points()
    time_list = []
    value_list = []
    for item in points:
        time_item = item["time"]
        value_item = item["value"]

        time_str = str(time_item)
        time_local = utc_to_local(time_str)

        time_local = time_local[10:]
        time_date = time_str[:10]

        if time.strftime('%Y-%m-%d') == time_date:
            print("Date Match---------->")

            time_list = time_list + [time_local]
            value_list = value_list + [value_item]

            print("Value:", item["value"], "LocalTime:", time_local)
        else:
            print("Cant Match----------X")
    print("TimeList: ", time_list)
    print("ValueList:", value_list)

    x_data = time_list
    y_data = value_list
    # y_data1 = value_list1

    c = (
        Line(init_opts=opts.InitOpts(
            width="1800px", height="500px", theme=ThemeType.WHITE
        )
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="测试"),
            tooltip_opts=opts.TooltipOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=3, color="#9966FF")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name="℃",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=3, color="#9966FF")
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
            linestyle_opts=opts.LineStyleOpts(width=3),
            color="orange",
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1, color="orange"),
        )
            .add_yaxis(
            series_name="温度传感器TS02",
            y_axis=y_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=3),
            color="orange",
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1, color="orange"),
        )
    )

    return HttpResponse(c.render_embed())
