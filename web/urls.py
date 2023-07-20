'''
Author: Misaki
Date: 2023-07-20 14:40:48
LastEditTime: 2023-07-20 15:30:36
LastEditors: Misaki
Description: 
'''
from django.contrib import admin
from django.urls import path, include
from web.views import account

urlpatterns = [
    path('register/', account.register, name='register')
]