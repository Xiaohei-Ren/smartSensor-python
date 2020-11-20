# coding: utf-8
# Author：renyuke
# Date ：2020/11/20 9:50
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
]