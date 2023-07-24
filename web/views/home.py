'''
Author: Misaki
Date: 2023-07-24 15:39:06
LastEditTime: 2023-07-24 15:45:12
LastEditors: Misaki
Description: 
'''

from django.shortcuts import render, HttpResponse, redirect

def index(request):
    
    return render(request, 'index.html')