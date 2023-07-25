'''
Author: Misaki
Date: 2023-07-24 16:24:32
LastEditTime: 2023-07-25 17:40:08
LastEditors: Misaki
Description: 
'''
import datetime
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from web import models

class AuthMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer = user_object

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

        if not request.tracer:
            return redirect('/login/')
        
        
