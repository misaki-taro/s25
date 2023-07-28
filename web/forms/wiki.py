'''
Author: Misaki
Date: 2023-07-29 00:23:05
LastEditTime: 2023-07-29 01:02:21
LastEditors: Misaki
Description: 
'''

from django import forms
from web import models
from web.forms.bootstrap import BootstrapForm
from django.core.exceptions import ValidationError

class WikiModelForm(BootstrapForm, forms.ModelForm):
    bootstrap_class_exclude = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = models.Wiki
        exclude = ['project', ]

