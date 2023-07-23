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
from utils import encrypt
import random
from django_redis import get_redis_connection
from web.forms.boostrap import BoostrapForm

class RegisterModelForm(BoostrapForm, forms.ModelForm):
    password = forms.CharField(
        label='密码', 
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': '密码长度不能小于8个字符',
            'max_length': '密码长度不能大于64个字符',
        },
        widget=forms.PasswordInput())

    comfirm_password = forms.CharField(
        label='重复密码', 
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': '重复密码长度不能小于8个字符',
            'max_length': '重复密码长度不能大于64个字符',
        },
        widget=forms.PasswordInput())

    mobile_phone = forms.CharField(label='手机号', 
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', 
                                                              '手机号格式错误')])

    code = forms.CharField(
        label='验证码', 
        widget=forms.TextInput)
                                                                  
    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'comfirm_password', 'mobile_phone', 'code']
    
    # # 为所有标签加上样式
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = '请输入{0}'.format(field.label)
    

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已经存在')

        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已经存在')
        return email
    
    def clean_password(self):
        password = self.cleaned_data['password']
        
        # 加密
        return encrypt.md5(password) 
    
    def clean_comfirm_password(self):
        password = self.cleaned_data['password']
        comfirm_password = encrypt.md5(self.cleaned_data['comfirm_password'])
        
        if password != comfirm_password:
            raise ValidationError('两次输入的密码不一样')
        
        return comfirm_password
    
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已存在')

        return mobile_phone
    
    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data['mobile_phone']
        if not mobile_phone:
            return code
        
        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        
        if not redis_code:
            raise ValidationError('验证码失效或者未发送，请重新发送')
        
        redis_str_code = redis_code.decode('utf-8')
        
        if code != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')
        
        return code

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
        if exists and tpl == 'register':
            raise ValidationError('手机号已存在')

        if not exists and tpl == 'login':
            raise ValidationError('手机号不存在')
        
        # # 校验发短信
        # send_sample = sms.Sample()
        # sign_name = 'mbug平台'
        # template_code = 'SMS_461960909'
        # random_code = str(random.randrange(1000, 9999))
        # template_param = '{code:' + random_code + '}'
        # return_sms = send_sample.send_single_message(mobile_phone, sign_name, template_code, template_param)
        # print(return_sms)
        # if return_sms is None:
        #     raise ValidationError('短信请求失败')
        # if return_sms['status'] != '3':
        #     raise ValidationError('短信发送失败: {0}'.format(return_sms['res']))
        
        # 假装验证码是1234
        return_sms = {
            'code': '1234'
        }

        # 验证码 写入redis（django-redis）
        conn = get_redis_connection()
        conn.set(mobile_phone, return_sms['code'], ex=60)
        
        
        return mobile_phone

class LoginSMSForm(BoostrapForm, forms.Form):
    mobile_phone = forms.CharField(label='手机号', 
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$','手机号格式错误')])

    code = forms.CharField(
        label='验证码', 
        widget=forms.TextInput) 
    
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exist = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if not exist:
            raise ValidationError('手机号不存在')
        return mobile_phone
    
    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data.get('mobile_phone')
        
        # 不存在手机号
        if not mobile_phone:
            return code
        
        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或者未发送，请重新发送')
        
        redis_str_code = redis_code.decode('utf-8')
        
        if code != redis_str_code:
            raise ValidationError('验证码错误')
        
        return code