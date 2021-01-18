"""SmartSensorSystem_renyk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from app_dashboard import views as dashboard_view
from app_user import views as user_view
from app_sensor_visual import views as sensor_view
from app_sensor_manage import views as sensor_manage_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_view.login),
    path('register/', user_view.register),
    path('user_info/', user_view.info),
    path('logout/', user_view.logout),
    path('dashboard/', dashboard_view.dashboard),
    path('', dashboard_view.dashboard),
    url(r'^sensor_detail/(\d+)', sensor_view.sensor_detail),
    path('sensor_add/', sensor_manage_view.add),
    path('sensor_list/', sensor_manage_view.sensor_list),
    path('sensor_list_temp/', sensor_manage_view.temp_sensor_list),
    path('sensor_list_pre/', sensor_manage_view.pre_sensor_list),
    path('sensor_list_flow/', sensor_manage_view.flow_sensor_list),
    path('sensor_list_con/', sensor_manage_view.con_sensor_list),
    path('sensor_list_ele/', sensor_manage_view.ele_sensor_list),
    path('sensor_add/', sensor_manage_view.add),
    path('sensor_temp_chart/', dashboard_view.sensor_temp_chart),
    path('visual_dashboard_screen/', dashboard_view.visual_dashboard),

    url(r'^time_list/$', dashboard_view.json_return_tl, name='time_list'),
    url(r'^value_list/$', dashboard_view.json_return_vl, name='value_list'),

    url(r'^time_list_2/$', dashboard_view.json_return_tl_2, name='time_list_2'),
    url(r'^value_list_2/$', dashboard_view.json_return_vl_2, name='value_list_2'),

    url(r'^time/$', dashboard_view.json_return_t, name='time'),
    url(r'^value/$', dashboard_view.json_return_v, name='value'),

    url(r'^time_list_id/$', sensor_view.return_id_tl, name='time_list_id'),
    url(r'^value_list_id/$', sensor_view.return_id_vl, name='value_list_id'),
    url(r'^time_id/$', sensor_view.return_id_t, name='time_id'),
    url(r'^value_id/$', sensor_view.return_id_v, name='value_id'),

    url(r'^test/$', sensor_manage_view.test, name='test'),
    url(r'^pre/$', dashboard_view.pressure_data, name='pre'),
    url(r'^pre_mid/$', dashboard_view.pressure_data_mid, name='pre_mid'),

]

