from django.shortcuts import render


# Create your views here.

def sensor_detail(request):
    return render(request, 'sensor_detail.html')
