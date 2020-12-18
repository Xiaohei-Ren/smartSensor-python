from django.shortcuts import render

# Create your views here.
import datetime
from random import randrange
import pytz
from django.http import HttpResponse
from influxdb import InfluxDBClient
import pyecharts.options as opts
import time

from pyecharts.commons.utils import JsCode
from rest_framework.views import APIView
from pandas.io import json
from pyecharts.charts import Line, Bar, Gauge, Grid, Liquid, Graph


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
            # markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=15, name="温度上限")],
            #                                 linestyle_opts=opts.LineStyleOpts(color="#f9a9af", type_="dashed")),
            # color="orange",
            areastyle_opts=opts.AreaStyleOpts(opacity=0.3, color="#fce3a8"),
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


def liquid() -> Grid:
    l1 = (
        Liquid()
            .add(
            "lq",
            [0.8],
            shape="path:// M128 938.666667v-47.530667h381.866667V863.573333a165.802667 165.802667 0 0 1-142.144-163.648V321.706667h-23.978667v-19.456h-50.069333a42.432 42.432 0 0 0-42.304 42.304V488.810667a93.290667 93.290667 0 0 1 66.666666 89.130666v194.474667a93.12 93.12 0 0 1-68.544 89.6v28.224h-46.933333v-27.733333a93.290667 93.290667 0 0 1-70.4-90.154667v-194.325333a93.290667 93.290667 0 0 1 62.805333-87.893334v-145.493333a98.432 98.432 0 0 1 29.76-70.570667 98.389333 98.389333 0 0 1 68.885334-28.053333h50.069333v-19.2h25.706667a165.802667 165.802667 0 0 1 163.541333-141.312 165.696 165.696 0 0 1 165.269333 165.269333v379.221334h24.96v23.701333h46.4V430.165333a83.456 83.456 0 0 1 83.2-83.2 83.456 83.456 0 0 1 83.2 83.2V784.426667a83.754667 83.754667 0 0 1-70.805333 82.261333v24.64h68.544v47.530667z m714.005333-47.530667v-24.405333a83.498667 83.498667 0 0 1-72.341333-82.496v-84.330667H723.2v24.256h-26.752a165.994667 165.994667 0 0 1-139.648 139.306667v27.733333z",
            center=["70%", "50%"],
            # outline_itemstyle_opts=opts.ItemStyleOpts(color="#74b9f0"),
            is_outline_show=False,
            label_opts=opts.LabelOpts(
                font_size=15,
                formatter='{@score}m³/h',
                position="inside",
                color="#74b9f0"
            ),
        )
        # .set_global_opts(title_opts=opts.TitleOpts(title="多个 Liquid 显示"))
    )

    l2 = Liquid().add(
        "流量",
        [0.67],
        shape="path:// M1050.615743 622.950934a234.158635 234.158635 0 0 1-5.952372-134.696418c10.336646-68.708294 22.657416-152.713545-84.677292-201.996625 7.072442-26.209638 6.784424-56.48353-15.008938-66.980186l-128.008-62.659916c-27.905744-13.696856-100.838302-10.816676-109.318833 7.20045s-32.002 55.619476 27.745734 69.572348 115.2072 85.157322 115.207201 85.157322a99.2062 99.2062 0 0 0 61.027814 32.002c71.652478 25.6016 67.84424 55.619476 56.931558 125.767861a307.219201 307.219201 0 0 0 11.904744 178.507157c38.658416 88.32552 41.058566 228.590287 7.52047 261.872367a101.190324 101.190324 0 0 1-131.2082 4.48028c-47.170948-32.002-48.003-179.467217-43.746734-272.657041a446.71592 446.71592 0 0 0-10.336646-154.153635 154.057629 154.057629 0 0 0-143.336959-104.454528h-46.466904V39.04244a38.850428 38.850428 0 0 0-38.4024-39.04244H115.229282a38.946434 38.946434 0 0 0-38.4024 39.04244v906.87268H38.424482a37.794362 37.794362 0 0 0-38.402401 39.04244v39.04244h689.579099v-39.04244a38.050378 38.050378 0 0 0-38.4024-39.04244h-38.4024V467.645228h46.018876a77.060816 77.060816 0 0 1 71.108444 51.587224 381.879867 381.879867 0 0 1 6.4004 125.479843c-4.256266 91.04569-8.928558 282.609663 78.020877 341.237327a196.268267 196.268267 0 0 0 109.60685 35.2022 164.394275 164.394275 0 0 0 117.831364-48.995062c85.989374-85.317332 29.793862-301.202825 8.832552-349.205826z m-174.474904-323.220201a19.52122 19.52122 0 1 1 19.2012-19.585224 19.2012 19.2012 0 0 1-19.233202 19.68123zM153.43967 116.903306a38.850428 38.850428 0 0 1 38.4024-39.04244h306.483155a38.946434 38.946434 0 0 1 38.4024 39.04244v233.838615a38.946434 38.946434 0 0 1-38.4024 39.042441H191.84207a38.754422 38.754422 0 0 1-38.4024-39.042441z",
        center=["25%", "50%"],
        is_outline_show=False,
        label_opts=opts.LabelOpts(
            font_size=15,
            formatter='{@score}m³/h',
            position="insideLeft",
            distance=60,
            color="#74b9f0"
        ),
    )

    grid = Grid().add(l1, grid_opts=opts.GridOpts()).add(l2, grid_opts=opts.GridOpts())
    ch = grid.dump_options_with_quotes()
    return ch


def liquid_1() -> Grid:
    l1 = (
        Liquid()
            .add(
            "lq",
            [0.8],
            shape="path:// M1986.296938 695.425728H1276.48679l-200.162853-0.316945h-55.904193c-146.135949 0-183.632961-130.48375-183.632961-275.912669v-62.29185c0-145.136354 37.789576-275.937049 183.632961-275.937049h965.877194c146.16033 0 183.632961 130.800695 183.632961 276.229614v62.31623c0 145.428918-37.472632 275.912669-183.632961 275.912669zM1719.405006 37.692055c0-20.893979 15.237732-37.692055 34.327564-37.692055h206.184805c19.065451 0 34.327564 16.798076 34.327564 37.692055v26.135759H1719.405006V37.692055z m-353.320349 0c0-20.893979 15.262113-37.692055 34.327564-37.692055h206.209185c19.065451 0 34.303183 16.798076 34.303183 37.692055v26.135759H1366.084657V37.692055z m-353.612914 0c0-20.893979 15.262113-37.692055 34.327564-37.692055h206.209185c19.04107 0 34.303183 16.798076 34.303183 37.692055v26.135759H1012.471743V37.692055z m230.662698 684.820266h924.893789v130.508131h-75.262208c0.926454 6.631461 1.560344 13.360444 1.560343 20.235709 0 83.161449-68.630747 150.402514-153.474441 150.402514-84.819314 0-153.450061-67.241066-153.45006-150.402514a145.867765 145.867765 0 0 1 1.487202-20.235709h-34.546987c0.950835 6.728983 1.584724 13.555487 1.584725 20.552653 0 83.161449-68.923311 150.402514-153.450061 150.402515-84.819314 0-153.450061-67.241066-153.450061-150.402515 0-6.997167 0.65827-13.823671 1.584724-20.552653H701.426958v-0.316945H438.972255c0.950835 6.728983 1.609105 13.555487 1.609104 20.552654 0 81.601105-66.412133 148.549606-149.963667 150.402514h-2.535559c-84.819314 0-153.474441-67.241066-153.474441-150.402514 0-6.997167 0.65827-13.823671 1.609105-20.552654H37.208106S1.295819 811.915145 0.028039 761.447775c-0.316945-15.554677 23.844004-28.646937 23.502679-46.395848-0.63389-83.478393-8.874455-285.274732 9.21578-329.183781 13.360444-31.767625 37.692055-62.608795 37.692055-62.608795L326.213035 31.767625h465.128735v690.744696h451.792671zM665.831615 146.282231h-172.613033c-54.465751 0-98.618604 43.665246-98.618604 97.521488v195.042975h271.231637V146.282231z",
            center=["70%", "50%"],
            # outline_itemstyle_opts=opts.ItemStyleOpts(color="#74b9f0"),
            is_outline_show=False,
            label_opts=opts.LabelOpts(
                font_size=15,
                formatter='{@score}m³/h',
                position="insideRight",
                distance=50,
                color="#74b9f0"
            ),
        )
        # .set_global_opts(title_opts=opts.TitleOpts(title="多个 Liquid 显示"))
    )

    l2 = Liquid().add(
        "流量",
        [0.67],
        shape="path:// M1247.085714 916.450743H1126.4v-161.792h80.457143c44.266057 0 80.457143-88.970971 80.457143-202.225372 0-113.225143-36.191086-202.196114-80.457143-202.196114H1126.4V228.907886c0-24.283429-16.091429-40.462629-40.228571-40.462629s-40.228571 16.1792-40.228572 40.462629v40.433371h-120.685714V204.624457l28.145371-28.320914c8.045714-8.074971 12.0832-16.149943 12.0832-28.291657V107.549257c24.137143 0 40.228571-16.149943 40.228572-40.433371 0-24.283429-16.091429-40.433371-40.228572-40.433372H643.657143c-24.137143 0-40.228571 16.1792-40.228572 40.433372 0 24.283429 16.091429 40.433371 40.228572 40.433371V148.041143c0 12.141714 4.008229 20.216686 12.0832 28.291657l28.145371 28.320914v64.7168H563.2V148.011886c0-24.283429-88.502857-40.462629-201.142857-40.462629S160.914286 123.757714 160.914286 148.041143v121.329371H80.457143C36.220343 269.341257 0 394.678857 0 552.433371c0 157.754514 36.220343 283.121371 80.457143 283.121372H160.914286v80.896H40.228571C16.091429 916.450743 0 932.600686 0 956.884114c0 24.283429 16.091429 40.433371 40.228571 40.433372h1206.857143c24.137143 0 40.228571-16.1792 40.228572-40.433372 0-24.283429-16.091429-40.433371-40.228572-40.433371zM965.485714 754.658743h-80.457143v-161.792H965.485714v161.792z m-241.371428 0v-161.792h80.457143v161.792h-80.457143z m-80.457143 0h-80.457143v-161.792H643.657143v161.792z m-80.457143 80.896h482.742857v80.896h-482.742857v-80.896z",
        center=["25%", "50%"],
        is_outline_show=False,
        label_opts=opts.LabelOpts(
            font_size=15,
            formatter='{@score}m³/h',
            position="inside",
            color="#74b9f0"
        ),
    )

    grid = Grid().add(l1, grid_opts=opts.GridOpts()).add(l2, grid_opts=opts.GridOpts())
    ch = grid.dump_options_with_quotes()
    return ch


def graph() -> Graph:
    nodes_data = [
        opts.GraphNode(name="氢气车", symbol_size=10, value=10),
        opts.GraphNode(name="加注机", symbol_size=20, value=20),
        opts.GraphNode(name="储氢罐", symbol_size=30, value=30),
        opts.GraphNode(name="压缩机", symbol_size=40, value=40),
        opts.GraphNode(name="长管拖车", symbol_size=40, value=50),
    ]
    links_data = [
        opts.GraphLink(source="氢气车", target="加注机", value=10),
        opts.GraphLink(source="加注机", target="储氢罐", value=10),
        opts.GraphLink(source="储氢罐", target="压缩机", value=10),
        opts.GraphLink(source="压缩机", target="长管拖车", value=10),
        opts.GraphLink(source="长管拖车", target="氢气车", value=10),
    ]
    c = (
        Graph()
            .add(
            "",
            nodes_data,
            links_data,
            repulsion=4000,
            is_draggable=True,
            # label_opts=opts.LabelOpts(
            #     formatter="压力：{@source} Mpa"
            # ),
            edge_label=opts.LabelOpts(
                is_show=True, position="middle", formatter="压差：{@source} Mpa"
            ),
            itemstyle_opts=opts.ItemStyleOpts(color='#4ed497')

        )
            # .set_global_opts(
            # title_opts=opts.TitleOpts(title="Graph-GraphNode-GraphLink-WithEdgeLabel")
        # )
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


class GaugeView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(temp_gauge()))


class BarView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(bar()))


class LiquidView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(liquid()))


class LiquidView_1(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(liquid_1()))


class GraphView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(graph()))


cnt = 9


class ChartUpdateView(APIView):
    def get(self, request, *args, **kwargs):
        global cnt
        cnt = cnt + 1
        return JsonResponse({"name": cnt, "value": randrange(0, 100)})


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/dashboard_2.html", 'rb').read())


class IndexView_1(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/visual_dashboard_screen.html", 'rb').read())