import json
from django.http import HttpResponse
from django.shortcuts import render
from pyecharts.charts import Grid, Line
import pyecharts.options as opts
from rest_framework.views import APIView
from app_sensor_manage.models import Sensor
from app_user import forms as user_form
from app_dashboard import views as dashboard_views


# Create your views here. todo：报警记录模块

def sensor_detail(request, id):
    # user = request.session['user_name']
    login_form = user_form.UserForm()
    if not request.session.get('is_login', None):
        message = '未登录，请登录！'
        return render(request, 'user_login.html', locals())

    sensor = Sensor.objects.get(id=id, delete=0)

    # 设置全局变量用于绘制图表
    id = int(id)
    global g_id
    g_id = id
    global g_name
    g_name = sensor.sensor_id
    global g_unit
    g_unit = sensor.unit

    # 获取实时传感器数据 todo:后端传值改为实时获取
    (time_list_res, value_list_res) = dashboard_views.data_reader(id)
    if not value_list_res == []:
        data_now = value_list_res[-1]

    return render(request, 'sensor_detail.html', locals())


g_id = 0
g_name = ""
g_unit = ""


def now_temp_line() -> Grid:
    """
    实时数据处理折线图绘制
    :return:
    """
    (time_list_res, value_list_res) = dashboard_views.data_reader(g_id)
    x_data = time_list_res
    y_data = value_list_res
    c = (
        Line(init_opts=opts.InitOpts())
            .set_global_opts(
            title_opts=opts.TitleOpts(title="实时数据", title_textstyle_opts=opts.TextStyleOpts(color="#505458"),
                                      pos_top=0, pos_left=0,),
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
            # datazoom_opts=[opts.DataZoomOpts(range_start=80, range_end=100)],
            toolbox_opts=opts.ToolboxOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name=g_unit,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=3, color="#74b9f0")
                )
            ),

        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name=g_name,
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
            .set_colors(["#fce3a8"])
    )
    grid = Grid()
    grid.add(c, grid_opts=opts.GridOpts(pos_left='3%', pos_right='2%', pos_bottom='8%', pos_top='25 %'))
    ch = grid.dump_options_with_quotes()
    return ch


def his_temp_line() -> Grid:
    """
    历史数据折线图可视化
    :return:
    """
    (time_list_res, value_list_res) = dashboard_views.data_reader_all(g_id)
    x_data = time_list_res
    y_data = value_list_res

    c = (
        Line(init_opts=opts.InitOpts())
            .set_global_opts(
            title_opts=opts.TitleOpts(title="历史数据", title_textstyle_opts=opts.TextStyleOpts(color="#505458"),
                                      pos_top=0, pos_left=0, ),
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
            datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100)],
            toolbox_opts=opts.ToolboxOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name=g_unit,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=3, color="#74b9f0")
                )
            ),

        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name=g_name,
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
            .set_colors(["#fce3a8"])
    )
    grid = Grid()
    grid.add(c, grid_opts=opts.GridOpts(pos_left='3%', pos_right='2%', pos_bottom='20%', pos_top='25 %'))
    ch = grid.dump_options_with_quotes()
    return ch


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


class ChartView_now(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(now_temp_line()))


class ChartView_his(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(his_temp_line()))


def sensor_temp_chart(request):
    return render(request, 'sensor_temp_chart.html')

def sensor_multi_chart(request):
    return render(request, 'sensor_multi_chart.html')
