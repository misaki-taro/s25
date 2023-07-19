from django.shortcuts import render

from django import forms
from app_01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

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
        fields = '__all__'
    
    # 为所有标签加上样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{0}'.format(field.label)
    

# Create your views here.
def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})
    