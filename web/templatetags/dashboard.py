'''
Author: Misaki
Date: 2023-08-10 10:01:35
LastEditTime: 2023-08-10 10:02:58
LastEditors: Misaki
Description: 
'''
from django.template import Library
from django.urls import reverse
from web import models

register = Library()


@register.simple_tag
def user_space(size):
    if size >= 1024 * 1024 * 1024:
        return "%.2f GB" % (size / (1024 * 1024 * 1024),)
    elif size >= 1024 * 1024:
        return "%.2f MB" % (size / (1024 * 1024),)
    elif size >= 1024:
        return "%.2f KB" % (size / 1024,)
    else:
        return "%d B" % size