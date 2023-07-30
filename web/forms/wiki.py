'''
Author: Misaki
Date: 2023-07-29 00:23:05
LastEditTime: 2023-07-29 11:31:26
LastEditors: Misaki
Description: 
'''

from django import forms
from web import models
from web.forms.bootstrap import BootstrapForm
from django.core.exceptions import ValidationError

class WikiModelForm(BootstrapForm, forms.ModelForm):
    bootstrap_class_exclude = []
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        total_list = [('', '请选择')]
        data_list = models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title')
        total_list.extend(data_list)
        self.fields['parent'].choices = total_list 
    class Meta:
        model = models.Wiki
        exclude = ['project', 'depth']

