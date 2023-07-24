'''
Author: Misaki
Date: 2023-07-20 14:40:48
LastEditTime: 2023-07-24 16:38:19
LastEditors: Misaki
Description: 
'''
from django.contrib import admin
from django.urls import path, include
from web.views import account, home

urlpatterns = [
    path('register/', account.register, name='register'),
    path('send/sms/', account.send_sms, name='send_sms'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/', account.login, name='login'),
    path('logout/', account.logout, name='logout'),
    path('image/code/', account.image_code, name='image_code'),
    path('index/', home.index, name='index'),
]