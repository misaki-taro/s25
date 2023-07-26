'''
Author: Misaki
Date: 2023-07-20 14:40:48
LastEditTime: 2023-07-26 16:46:48
LastEditors: Misaki
Description: 
'''
from django.contrib import admin
from django.urls import path, include, re_path
from web.views import account, home, project

urlpatterns = [
    path('register/', account.register, name='register'),
    path('send/sms/', account.send_sms, name='send_sms'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/', account.login, name='login'),
    path('logout/', account.logout, name='logout'),
    path('image/code/', account.image_code, name='image_code'),
    path('index/', home.index, name='index'),
    path('project/list/', project.project_list, name='project_list'),
    re_path(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    re_path(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),
]