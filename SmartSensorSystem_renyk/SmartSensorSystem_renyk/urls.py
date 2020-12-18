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
    path('test/', user_view.test),
    path('', user_view.test),
    url(r'^line/$', dashboard_view.ChartView.as_view()),
    url(r'^gauge/$', dashboard_view.GaugeView.as_view()),
    url(r'^bar/$', dashboard_view.BarView.as_view()),
    url(r'^liquid/$', dashboard_view.LiquidView.as_view()),
    url(r'^liquid_1/$', dashboard_view.LiquidView_1.as_view()),
    url(r'^graph/$', dashboard_view.GraphView.as_view()),
    url(r'^lineUpdate/$', dashboard_view.ChartUpdateView.as_view()),
    url(r'^dashboard/$', dashboard_view.IndexView.as_view()),
    url(r'^sensor_detail/(\d+)', sensor_view.sensor_detail),
    path('sensor_add/', sensor_manage_view.add),
    path('sensor_list/', sensor_manage_view.sensor_list),
    path('sensor_list_temp/', sensor_manage_view.temp_sensor_list),
    path('sensor_list_pre/', sensor_manage_view.pre_sensor_list),
    path('sensor_list_flow/', sensor_manage_view.flow_sensor_list),
    path('sensor_list_con/', sensor_manage_view.con_sensor_list),
    path('sensor_list_ele/', sensor_manage_view.ele_sensor_list),
]
