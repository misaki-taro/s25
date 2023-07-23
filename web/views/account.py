'''
Author: Misaki
Date: 2023-07-20 15:23:57
LastEditTime: 2023-07-21 12:19:51
LastEditors: Misaki
Description: 
'''
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from web.forms import account

def register(request):
    if request.method == 'GET':
        form = account.RegisterModelForm()
        return render(request, 'register.html', {'form': form}) 
    form = account.RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})

def send_sms(request):
    form = account.SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def login_sms(request):
    # GET 为显示页面
    if request.method == 'GET':
        form = account.LoginSMSForm()
        return render(request, 'login.html', {'form': form})
    
    # POST 为登录提交表单
    form = account.LoginSMSForm(request.POST)
    if form.is_valid():
        mobile_phone = form.cleaned_data['mobile_phone']
        
        # 写入session
        print(mobile_phone)
        
        return JsonResponse({'status': True, 'data': '/index/'})
    
    return JsonResponse({'status': False, 'error': form.errors})
    