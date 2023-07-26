'''
Author: Misaki
Date: 2023-07-26 11:17:02
LastEditTime: 2023-07-26 12:29:27
LastEditors: Misaki
Description: 
'''
from django import forms
from web import models
from web.forms.bootstrap import BootstrapForm
from django.core.exceptions import ValidationError

class ProjectModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea,
        }
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    
    
    # 钩子来验证
    def clean_name(self):
        name = self.cleaned_data['name']
        
        # 如果这个用户的项目名存在就返回错误信息
        exist = models.Project.objects.filter(name=name, creator=self.request.tracer.user).exists()
        if exist:
            raise ValidationError('项目已存在')
        
        # 如果项目数超过了就返回错误信息
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()
        
        if(count >= self.request.tracer.price_policy.project_num):
            raise ValidationError('项目个数超限，请购买套餐')
        
        return name