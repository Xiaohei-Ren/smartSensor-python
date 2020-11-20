# coding: utf-8
# Author：renyuke
# Date ：2020/11/20 16:05

from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=256, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
