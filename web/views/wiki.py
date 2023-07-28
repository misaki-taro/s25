'''
Author: Misaki
Date: 2023-07-28 23:38:37
LastEditTime: 2023-07-29 01:04:28
LastEditors: Misaki
Description: 
'''
from django.shortcuts import render, redirect
from web.forms.wiki import WikiModelForm
from django.urls import reverse

def wiki(request, project_id):
    print('here')
    return render(request, 'wiki.html')

def wiki_add(request, project_id):
    print('here wikiadd')
    # 展示页面
    if request.method == 'GET':
        form = WikiModelForm()
        return render(request, 'wiki_add.html', {'form': form})
    
    form = WikiModelForm(data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.save()
        url = reverse('web:manage:wiki_add', kwargs={'project_id': project_id})
        return redirect(url)

    return render(request, 'wiki_add.html', {'form': form})