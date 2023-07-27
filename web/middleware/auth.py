'''
Author: Misaki
Date: 2023-07-24 16:24:32
LastEditTime: 2023-07-27 16:33:34
LastEditors: Misaki
Description: 
'''
import datetime
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.conf import settings

from web import models
from web import views

class Tracer(object):
    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleware(MiddlewareMixin):
    
    def process_request(self, request):

        request.tracer = Tracer()
        
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object

        # 如果url在白名单，直接返回
        wrul = settings.WHITE_REGEX_URL_LIST
        print(request.path_info)
        if request.path_info in wrul:
            return

        # 根据用户选择最新的交易记录
        _object = models.Transaction.objects.filter(user=user_object).order_by('-id').first()
        cur_time = datetime.datetime.now()
        if _object.end_datetime and (_object.end_datetime < cur_time):
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()
        
        request.tracer.price_policy = _object.price_policy
        
        
        # 根据过期时间来确定额度是否降级

        if not request.tracer.user:
            return redirect('/login/')

    def process_view(self, request, view, args, kwargs):
        if not request.path_info.startswith('/manage/'):
            return
        
        project_id = kwargs.get('project_id')
        
        project_object = models.Project.objects.filter(creator=request.tracer.user, id=project_id).first()
        if project_object:
            request.tracer.project = project_object
            return
        
        project_user_object = models.ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_user_object:
            # 是我参与的项目
            request.tracer.project = project_user_object.project
            return

        return redirect(reverse(views.project.project_list))
        
        
