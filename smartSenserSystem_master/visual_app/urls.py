# coding: utf-8
# Author：renyuke
# Date ：2020/11/11 21:53
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^line/$', views.ChartView.as_view(), name='visual_app'),
    url(r'^lineUpdate/$', views.ChartUpdateView.as_view(), name='visual_app'),
    url(r'^index/$', views.IndexView.as_view(), name='visual_app'),
]
