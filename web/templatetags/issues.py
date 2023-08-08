'''
Author: Misaki
Date: 2023-08-08 16:03:05
LastEditTime: 2023-08-08 16:03:08
LastEditors: Misaki
Description: 
'''

from django.template import Library
from django.urls import reverse
from web import models
from web import views

register = Library()

@register.simple_tag
def string_just(num):
    if num < 100:
        num = str(num).rjust(3, "0")
    return "#{}".format(num)

