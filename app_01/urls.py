'''
Author: Misaki
Date: 2023-07-20 14:40:48
LastEditTime: 2023-07-20 14:42:07
LastEditors: Misaki
Description: 
'''
from django.contrib import admin
from django.urls import path, include
from app_01 import views

urlpatterns = [
    path('register/', views.register, name='register')
]

