import hashlib
import re
from django.shortcuts import render, redirect
from django.utils import timezone
from app_user import forms, models


# Create your views here.


def login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if request.session.get('is_login', None):
            message = '不能重复登录！'
            return render(request, 'user_login.html', locals())
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # 数据验证
            try:
                user = models.User.objects.get(name=username, delete=0)
            except:
                message = '用户不存在！'
                return render(request, 'user_login.html', locals())
            if user.password == hash_code(password):
                # session写入
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_role'] = user.role
                models.User.objects.filter(name=username).update(last_login_time=timezone.now())
                return redirect('/test/')
            else:
                message = '密码不正确！'
                return render(request, 'user_login.html', locals())
        else:
            return render(request, 'user_login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'user_login.html', locals())


def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    login_form = forms.UserForm()
    if not request.session.get('is_login', None):
        message = '未登录，请登录！'
        return render(request, 'user_login.html', locals())
    if not request.session['user_role'] == 'admin':
        message = '无注册新用户权限，权限请使用管理员账号登录后注册!'
        return render(request, 'user_login.html', locals())
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
            # 参数校验
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
                # 执行事务
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
    """
    用户登出
    :param request:
    :return:
    """
    login_form = forms.UserForm()
    if not request.session.get('is_login', None):
        message = '未登录，请登录！'
        return render(request, 'user_login.html', locals())
    request.session.flush()
    return render(request, 'user_logout.html', locals())


def info(request):
    """
    用户信息
    :param request:
    :return:
    """
    login_form = forms.UserForm()
    if not request.session.get('is_login', None):
        message = '未登录，请登录！'
        return render(request, 'user_login.html', locals())
    current_user_id = request.session['user_id']
    names = models.User.objects.get(id=current_user_id)
    return render(request, 'user_info.html', locals())


def hash_code(s, salt='login'):
    """
    密码加密
    :param s:
    :param salt:
    :return:
    """
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def test(request):
    """
    dashboard主页
    :param request:
    :return:
    """
    return render(request, "dashboard_2.html")
