'''
Author: Misaki
Date: 2023-07-25 15:56:27
LastEditTime: 2023-07-25 15:58:17
LastEditors: Misaki
Description: 
'''

from django.shortcuts import render

def project_list(request):
    
    return render(request, 'project_list.html')
