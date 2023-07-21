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
    form = account.RegisterModelForm()
    return render(request, 'register.html', {'form': form}) 

def send_sms(request):
    form = account.SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})