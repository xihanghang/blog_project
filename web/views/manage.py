

from django.shortcuts import render

def dashboard(request,project_id):
    return render(request,'dashboard.html')

def issues(request,project_id):
    return render(request,'issues.html')

def statistic(request,project_id):
    return render(request,'statistic.html')
