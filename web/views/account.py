'''
Author: Misaki
Date: 2023-07-20 15:23:57
LastEditTime: 2023-07-24 16:41:10
LastEditors: Misaki
Description: 
'''
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from web.forms import account
from utils.image_code import check_code
from django.db.models import Q
from web import models

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
        return render(request, 'login_sms.html', {'form': form})
    
    # POST 为登录提交表单
    form = account.LoginSMSForm(request.POST)
    if form.is_valid():
        mobile_phone = form.cleaned_data['mobile_phone']
        
        # 写入session
        user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        request.session['user_id'] = user_object.id
        request.session.set_expiry(60 * 60 * 24 * 14)
        
        return JsonResponse({'status': True, 'data': '/index/'})
    
    return JsonResponse({'status': False, 'error': form.errors})

def login(request):
    if request.method == 'GET':
        form = account.LoginForm(request)
        return render(request, 'login.html', {'form': form})
    
    form = account.LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username'] # 得到是邮箱地址或者手机号
        password = form.cleaned_data['password']
        
        # 用Q做复杂查询
        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(password=password).first()
        
        if user_object:
            # 写入 session
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('/index/')
        
        form.add_error('username', '用户名或密码错误')
    
    return render(request, 'login.html', {'form': form})

def image_code(request):
    image_object, code = check_code()

    # 设置超时
    request.session['image_code'] = code
    request.session.set_expiry(60)

    from io import BytesIO
    # 存到内存中
    stream = BytesIO()
    image_object.save(stream, 'png')

    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.flush()
    return redirect('/index/')
    