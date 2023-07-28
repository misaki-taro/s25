'''
Author: Misaki
Date: 2023-07-27 14:53:47
LastEditTime: 2023-07-29 00:21:07
LastEditors: Misaki
Description: 
'''
from django.shortcuts import render

def dashboard(request, project_id):
    
    return render(request, 'dashboard.html')

def issues(request, project_id):
    
    return render(request, 'issues.html')
    
def statistics(request, project_id):
    
    return render(request, 'statistics.html')

def file(request, project_id):
    
    return render(request, 'file.html')


def setting(request, project_id):
    
    return render(request, 'setting.html')