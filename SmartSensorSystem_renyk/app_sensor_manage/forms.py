# coding: utf-8
# Author：renyuke
# Date ：2020/12/17 10:10

from django import forms


class SensorAddForm(forms.Form):
    sensor_id = forms.CharField(label='传感器编号', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Sensor_Id"}))
    name = forms.CharField(label='传感器名称', max_length=128, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Sensor_Name"}))
    sort = forms.CharField(label='传感器类别', max_length=128, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Sensor_Sort"}))
    location = forms.CharField(label='所在位置', max_length=128, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Sensor_Location"}))
    comment = forms.CharField(label='备注', max_length=128, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': "Sensor_Comment"}))
