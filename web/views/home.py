

from django.shortcuts import render


def index(request):
    return render(request,'index.html')

def control_center(request):
    return render(request,'contr_center.html')