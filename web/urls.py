'''
Author: Misaki
Date: 2023-07-20 14:40:48
LastEditTime: 2023-07-29 00:57:25
LastEditors: Misaki
Description: 
'''
from django.contrib import admin
from django.urls import path, include, re_path
from web.views import account, home, project, manage, wiki

urlpatterns = [
    path('register/', account.register, name='register'),
    path('send/sms/', account.send_sms, name='send_sms'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/', account.login, name='login'),
    path('logout/', account.logout, name='logout'),
    path('image/code/', account.image_code, name='image_code'),
    path('index/', home.index, name='index'),
    path('project/list/', project.project_list, name='project_list'),

    # 项目
    re_path(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    re_path(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),

    # 项目里
    re_path(r'^manage/(?P<project_id>\d+)/', include((
        [
            re_path(r'^dashboard/', manage.dashboard, name='dashboard'),
            re_path(r'^issues/', manage.issues, name='issues'),
            re_path(r'^statistics/', manage.statistics, name='statistics'),
            re_path(r'^file/', manage.file, name='file'),

            # wiki
            path('wiki/', wiki.wiki, name='wiki'),
            path('wiki/add/', wiki.wiki_add, name='wiki_add'),

            re_path(r'^setting/', manage.setting, name='setting'),
        ], 'manage'), namespace='manage')),   
]