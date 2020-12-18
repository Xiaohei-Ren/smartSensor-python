from django.shortcuts import render

from app_sensor_manage.models import Sensor
from app_user import forms as user_form


# Create your views here.

def sensor_detail(request, id):
    login_form = user_form.UserForm()
    if not request.session.get('is_login', None):
        message = '未登录，请登录！'
        return render(request, 'user_login.html', locals())
    print(id)
    sensor = Sensor.objects.get(id=id, delete=0)
    print(sensor)
    return render(request, 'sensor_detail.html', locals())
