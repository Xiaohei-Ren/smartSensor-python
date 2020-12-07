import hashlib
import re

from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone

from app_user import forms, models


def login(request):
    """
    用户登录
    :param request:
    :return:
    """
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
                return render(request, 'user_login.html', {'message': message, 'login_form': login_form})
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                # session写入
                current_user_now = models.CurrentUser.objects.filter(login=1)
                if current_user_now:
                    message = '不能重复登录！'
                    return render(request, 'user_login.html', {'message': message, 'login_form': login_form})
                current_user = models.CurrentUser()
                current_user.user_no = user.id
                current_user.update_time = timezone.now()
                current_user.login = 1
                current_user.save()

                models.User.objects.filter(name=username).update(last_login_time=timezone.now())
                return redirect('/user_info/')
            else:
                message = '密码不正确！'
                return render(request, 'user_login.html', {'message': message, 'login_form': login_form})
        else:
            return render(request, 'user_login.html', {'message': message, 'login_form': login_form})

    login_form = forms.UserForm()
    return render(request, 'user_login.html', {'login_form': login_form})


def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            phone_number = register_form.cleaned_data.get('phone_number')
            role = '普通用户'

            res = re.match('^[a-zA-Z]\w{5,17}$', password1)
            if not res:
                message = '格式必须为：以字母开头，长度在6~18之间，只能包含字符、数字和下划线！'
                return render(request, 'user_register.html', locals())
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'user_register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'user_register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'user_register.html', locals())

                res = re.match('1[3|4|5|7|8][0-9]\d{8}', phone_number)
                if not res:
                    message = '手机号格式错误！'
                    return render(request, 'user_register.html', locals())
                same_phone_number_user = models.User.objects.filter(phone_number=phone_number)
                if same_phone_number_user:
                    message = '该电话号码已经被注册！'
                    return render(request, 'user_register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.phone_number = phone_number
                new_user.role = role
                new_user.create_time = timezone.now()
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'user_register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'user_register.html', locals())


def logout(request):
    login_form = forms.UserForm()
    try:
        current_user = models.CurrentUser.objects.get(login=1)
    except:
        message = '未登录，请登录'
        return render(request, 'user_login.html', locals())
    current_user_now = models.CurrentUser.objects.get(login=1)
    current_user_now.login = 0
    current_user_now.save()

    logout_recode = models.CurrentUser()
    logout_recode.user_no = current_user.user_no
    logout_recode.logout = 1
    logout_recode.update_time = timezone.now()
    logout_recode.save()
    message = '登出成功！'
    return render(request, 'user-logout.html', locals())


def info(request):
    login_form = forms.UserForm()
    try:
        current_user = models.CurrentUser.objects.get(login=1)
    except:
        message = '未登录，请登录'
        return render(request, 'user_login.html', locals())
    current_user_id = current_user.user_no
    print(current_user_id)
    names = models.User.objects.get(id=current_user_id)

    login_recodes = models.CurrentUser.objects.filter(user_no=current_user_id, logout=0)[:5]

    logout_recodes = models.CurrentUser.objects.filter(user_no=current_user_id, logout=1)[:5]

    return render(request, 'user_info.html', locals())


def hash_code(s, salt='login'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
