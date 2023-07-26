'''
Author: Misaki
Date: 2023-07-25 15:56:27
LastEditTime: 2023-07-26 16:39:57
LastEditors: Misaki
Description: 
'''

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from web.forms import project
from web import models

def project_list(request):
    # project_list页面
    if request.method == 'GET':
        form = project.ProjectModelForm(request)

        project_dict = {'star': [], 'my': [], 'join': []}
        # 从数据库获取：创建的项目，参与的项目
        project_objects = models.Project.objects.filter(creator=request.tracer.user)
        project_user_objects = models.ProjectUser.objects.filter(user=request.tracer.user)
        
        for p in project_objects:
            if p.star:
                project_dict['star'].append({'value':p, 'type': 'my'})
            else:
                project_dict['my'].append(p)
        
        
        for p in project_user_objects:
            if p.star:
                project_dict['star'].append({'value': p.project, 'type': 'join'})
            else:
                project_dict['join'].append(p.project)
        
        
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})

    # POST => 创建projecct
    form = project.ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # form没包含这个字段，需要自己写入
        form.instance.creator = request.tracer.user
        
        # 写入数据库
        form.save()

        return JsonResponse({'status': True})
    
    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        print(reverse('web:project_list'))
        return redirect(reverse('web:project_list'))

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect(reverse('web:project_list'))
    
    return HttpResponse('请求错误')


def project_unstar(request, project_type, project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        print(reverse('web:project_list'))
        return redirect(reverse('web:project_list'))

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect(reverse('web:project_list'))
    
    return HttpResponse('请求错误')
