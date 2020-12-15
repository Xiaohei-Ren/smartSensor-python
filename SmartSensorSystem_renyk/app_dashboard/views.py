from django.shortcuts import render

# Create your views here.
import datetime
from random import randrange
import pytz
from django.http import HttpResponse
from influxdb import InfluxDBClient
import pyecharts.options as opts
import time
from rest_framework.views import APIView
from pandas.io import json
from pyecharts.charts import Line, Bar, Gauge, Grid


def con_DB(query):
    """
    influx数据库连接
    :param query:
    :return:
    """
    InfluxClient = InfluxDBClient('localhost', 8086, 'root', '123456', 'test')
    clientList = InfluxClient.get_list_database()
    # print("----------Connect Success----------")
    # print("clientList:", clientList)
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
        query = 'select "time","id", "value" from sensor01 where id=1;'
    elif id == 2:
        query = 'select "time","id", "value" from sensor01 where id=2;'
    Data = con_DB(query)
    # print(Data)
    points = Data.get_points()
    time_list = []
    value_list = []
    for item in points:
        time_item = item["time"]
        value_item = item["value"]

        time_str = str(time_item)
        time_local = utc_to_local(time_str)

        # 计算时间差，如果时间差大于一天就出队列
        time_now = datetime.datetime.now()
        time_com = time_now + datetime.timedelta(hours=0)
        time_com.ctime()
        time_com = str(time_com)
        time_com = time_com[:19]
        time_com = datetime.datetime.strptime(time_com, "%Y-%m-%d %H:%M:%S")
        # print("time_now:", time_com)

        time_local = time_local[:19]
        time_array = datetime.datetime.strptime(time_local, "%Y-%m-%d %H:%M:%S")
        # print("time_before", time_array)

        gap = (time_com - time_array).days
        # time_test = "2020-12-1 10:11:19"
        # time_test = datetime.datetime.strptime(time_test, "%Y-%m-%d %H:%M:%S")
        # print(time_com)
        # print(time_test)
        # gap = (time_com - time_test).days

        # print("gap:", gap)

        # if gap >= 1:
        #     pop

        time_local = time_local[10:]
        time_list = time_list + [time_local]
        value_list = value_list + [value_item]

    #     print("Value:", item["value"], "LocalTime:", time_local)
    # print("TimeList: ", time_list)
    # print("ValueList:", value_list)
    return time_list, value_list


def temp_line() -> Grid:
    """
    数据处理折线图绘制
    :return:
    """
    (time_list_res, value_list_res) = data_reader(1)
    x_data = time_list_res
    y_data = value_list_res
    # print(x_data)
    # print(y_data)
    # y_data1 = value_list1

    c = (
        Line(init_opts=opts.InitOpts())
            .set_global_opts(
            # title_opts=opts.TitleOpts(title="实时温度", title_textstyle_opts=opts.TextStyleOpts(color="#36404e"),
            #                           pos_top=0, pos_left=8,),
            tooltip_opts=opts.TooltipOpts(is_show=True, trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(is_show=True, selected_mode=False, item_height=15,
                                        pos_top=0,
                                        textstyle_opts=opts.TextStyleOpts(
                                            color="#74b9f0"
                                        )
                                        ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=3, color="#74b9f0", )
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
                    linestyle_opts=opts.LineStyleOpts(width=3, color="#74b9f0")
                )
            ),

        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="温度传感器TS01",
            y_axis=y_data,
            symbol="emptyCircle",
            is_symbol_show=False,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=3, color="#fce3a8"),
            # color="orange",
            areastyle_opts=opts.AreaStyleOpts(opacity=0.1, color="#fce3a8"),
        )
            #     .add_yaxis(
            #     series_name="温度传感器TS02",
            #     y_axis=y_data1,
            #     symbol="emptyCircle",
            #     is_symbol_show=True,
            #     is_smooth=True,
            #     label_opts=opts.LabelOpts(is_show=False),
            #     linestyle_opts=opts.LineStyleOpts(width=3, color="blue"),
            #     # color="pink",
            #     areastyle_opts=opts.AreaStyleOpts(opacity=0.1, color="blue"),
            # )
            .set_colors(["#fce3a8"])

            # .dump_options_with_quotes()
    )
    # print("Line done >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    grid = Grid()
    grid.add(c, grid_opts=opts.GridOpts(pos_left='3%', pos_right='3%', pos_bottom='6%'))
    ch = grid.dump_options_with_quotes()
    return ch


def temp_gauge() -> Gauge:
    (time_list_res, value_list_res) = data_reader(1)
    data = value_list_res[-1]
    c = (
        Gauge()
            .add(
            "温度传感器TS01",
            [("温度传感器TS01", data)],
            split_number=5,
            max_=60,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[(0.3, "#fcde97"), (0.7, "#74b9ed"), (1, "#f9a9af")], width=25,
                )
            ),
            detail_label_opts=opts.LabelOpts(formatter="{value}Mpa", font_size=15),
            title_label_opts=opts.GaugeTitleOpts(is_show=False, color="#9966FF")
        )
            .set_global_opts(
            # title_opts=opts.TitleOpts(title="实时气压", title_textstyle_opts=opts.TextStyleOpts(color="#36404e"),
            #                           pos_top=5, pos_left=8),
            legend_opts=opts.LegendOpts(is_show=False, selected_mode=False, item_height=15,
                                        pos_bottom=0,
                                        textstyle_opts=opts.TextStyleOpts(
                                            color="#36404e"
                                        )),
        )
            .dump_options_with_quotes()
    )
    # print("Gauge done >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    return c


def bar() -> Bar:
    c = (
        Bar()
            .add_xaxis([1, 2, 3])
            .add_yaxis("商家A", [1, 2, 3],
                       color="#67e0e3"
                       )
            .add_yaxis("商家B", [1, 2, 4],
                       color="#fd666d"
                       )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="柱形图",
                                      title_textstyle_opts=opts.TextStyleOpts(color="#9966FF"), pos_top=5, pos_left=8),
            yaxis_opts=opts.AxisOpts(name="Y 轴",
                                     axisline_opts=opts.AxisLineOpts(
                                         linestyle_opts=opts.LineStyleOpts(width=3, color="#9966FF")
                                     )
                                     ),
            xaxis_opts=opts.AxisOpts(name="X 轴",
                                     axisline_opts=opts.AxisLineOpts(
                                         linestyle_opts=opts.LineStyleOpts(width=3, color="#9966FF")
                                     )
                                     ),
        )
            .dump_options_with_quotes()
    )
    # print("Bar done >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
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


class GaugeView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(temp_gauge()))


class BarView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(bar()))


cnt = 9


class ChartUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        global cnt
        cnt = cnt + 1
        return JsonResponse({"name": cnt, "value": randrange(0, 100)})


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/dashboard_2.html", 'rb').read())
