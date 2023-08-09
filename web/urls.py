'''
Author: Misaki
Date: 2023-07-20 14:40:48
LastEditTime: 2023-08-09 19:41:38
LastEditors: Misaki
Description: 
'''
from django.contrib import admin
from django.urls import path, include, re_path
from web.views import account, home, project, manage, wiki, file, setting, issues

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
            # re_path(r'^issues/', manage.issues, name='issues'),
            re_path(r'^statistics/', manage.statistics, name='statistics'),

            # wiki
            path('wiki/', wiki.wiki, name='wiki'),
            path('wiki/add/', wiki.wiki_add, name='wiki_add'),
            path('wiki/catalog/', wiki.catalog, name='wiki_catalog'),
            path('wiki/delete/<int:wiki_id>/', wiki.wiki_delete, name='wiki_delete'),
            path('wiki/edit/<int:wiki_id>/', wiki.wiki_edit, name='wiki_edit'),
            path('wiki/upload/', wiki.wiki_upload, name='wiki_upload'),
            
            # file
            path('file/', file.file, name='file'),
            path('file/delete/', file.file_delete, name='file_delete'),
            path('cos/credential/', file.cos_credential, name='cos_credential'),
            path('file/post/', file.file_post, name='file_post'),
            path('file/download/<int:file_id>', file.file_download, name='file_download'),

            # setting
            path('setting/', setting.setting, name='setting'),
            path('setting/delete/', setting.delete, name='setting_delete'),

            # issues
            path('issues/', issues.issues, name='issues'),
            path('issues/detail/<int:issues_id>', issues.issues_detail, name='issues_detail'),
            path('issues/record/<int:issues_id>', issues.issues_record, name='issues_record'),
            path('issues/change/<int:issues_id>', issues.issues_change, name='issues_change'),
            path('issues/invite/url/', issues.invite_url, name='invite_url'),
            
            

            # re_path(r'^setting/', manage.setting, name='setting'),
        ], 'manage'), namespace='manage')),   
    
    path('invite/join/<str:code>', issues.invite_join, name='invite_join'),
]