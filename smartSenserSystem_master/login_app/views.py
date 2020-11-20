from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from login_app import models
from . import forms


def login(request):
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # 数据验证

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', {'message': message, 'login_form': login_form})
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                # session写入
                return render(request, 'index.html')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', {'message': message, 'login_form': login_form})
        else:
            return render(request, 'login/login.html', {'message': message, 'login_form': login_form})

    login_form = forms.UserForm()
    return render(request, 'login/login.html', {'login_form': login_form})


def register(request):
    return render(request, 'login/register.html')


def logout(request):
    return redirect("/login/")
