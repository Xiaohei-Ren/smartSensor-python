# coding: utf-8
# Author：renyuke
# Date ：2020/11/20 16:05

from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=256, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))


class RegisterForm(forms.Form):
    gender = (
        ('admin', "管理员"),
        ('user', "用户"),
    )
    username = forms.CharField(label="用户名", max_length=256,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username"}))
    password1 = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    email = forms.EmailField(label="邮箱地址",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Email"}))
    phone_number = forms.CharField(label="手机号码", max_length=256, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Phone Number"}))
