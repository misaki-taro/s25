'''
Author: Misaki
Date: 2023-07-20 15:58:24
LastEditTime: 2023-07-21 13:59:56
LastEditors: Misaki
Description: 
'''

from django.shortcuts import render

from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from utils.ali import sms
import random
from django_redis import get_redis_connection

class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号', 
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', 
                                                              '手机号格式错误')])
    password = forms.CharField(
        label='密码', 
        widget=forms.PasswordInput())
    comfirm_password = forms.CharField(
        label='重复密码', 
        widget=forms.PasswordInput())
    code = forms.CharField(
        label='验证码', 
        widget=forms.TextInput)
                                                                  
    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'comfirm_password', 'mobile_phone', 'code']
    
    # 为所有标签加上样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{0}'.format(field.label)

class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', 
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', 
                                                              '手机号格式错误')])
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.request = request
    
    # 钩子函数的作用就是 监听某个东西是否符合预期，不符合的话在中间截断不让到达目标
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        
        # 判断短信模板是否有问题
        tpl = self.request.GET['tpl']
        print(tpl)
        template_id = settings.ALI_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError('短信模板错误')
        
        # 校验数据库是否有手机号
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已存在')
        
        # # 校验发短信
        # send_sample = sms.Sample()
        # sign_name = 'mbug平台'
        # template_code = 'SMS_461960909'
        # template_param = '{code:12345}'
        # return_sms = send_sample.send_single_message(mobile_phone, sign_name, template_code, template_param)
        # print(return_sms)
        # if return_sms is None:
        #     raise ValidationError('短信请求失败')
        # if return_sms['status'] != '3':
        #     raise ValidationError('短信发送失败: {0}'.format(return_sms['res']))

        # # 验证码 写入redis（django-redis）
        # conn = get_redis_connection()
        # conn.set(mobile_phone, return_sms['code'], ex=60)
        
        
        return mobile_phone