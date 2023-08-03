'''
Author: Misaki
Date: 2023-08-03 17:07:40
LastEditTime: 2023-08-03 17:22:55
LastEditors: Misaki
Description: 
'''


from genericpath import exists
from django import forms
from web import models
from web.forms.bootstrap import BootstrapForm
from django.core.exceptions import ValidationError

class FileModelForm(BootstrapForm, forms.ModelForm):
    bootstrap_class_exclude = []
    
    def __init__(self, request, parent_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.parent_object = parent_object
    
    class Meta:
        model = models.FileRepository
        fields = ['name']

    # 钩子
    # 不能有重名的文件夹
    def clean_name(self):
        name = self.cleaned_data['name']
        
        queryset = models.FileRepository.objects.filter(file_type=2, name=name, project=self.request.tracer.project)
        if self.parent_object:
            exists = queryset.filter(parent=self.parent_object).exists()
        else:
            exists = queryset.filter(parent__isnull=True).exists()
        
        if exists:
            raise ValidationError('文件夹已存在')
        
        return name