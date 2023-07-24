'''
Author: Misaki
Date: 2023-07-24 16:24:32
LastEditTime: 2023-07-24 16:27:44
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
