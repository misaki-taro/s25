'''
Author: Misaki
Date: 2023-08-08 10:24:30
LastEditTime: 2023-08-08 20:17:25
LastEditors: Misaki
Description: 
'''


from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from web.forms.issues import IssuesModelForm, IssuesReplyModelForm
from web import models
from utils import pagination
from django.views.decorators.csrf import csrf_exempt

def issues(request, project_id):
    if request.method == 'GET':

        queryset = models.Issues.objects.filter(project_id=project_id)
        page_object = pagination.Pagination(
            current_page=request.GET.get('page'),
            all_count = queryset.count(),
            base_url = request.path_info,
            query_params = request.GET,
            per_page=1
        )
        
        issues_object_list = queryset[page_object.start: page_object.end] 
        # issues_object_list = queryset

        form = IssuesModelForm(request)
        context = {
            'form': form, 
            'issues_object_list': issues_object_list,
            'page_html': page_object.page_html()
        }

        return render(request, 'issues.html', context)
    
    form = IssuesModelForm(request, data=request.POST)
    
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True})
        
    return JsonResponse({'status': False, 'error':form.errors})

def issues_detail(request, project_id, issues_id):
    issues_object = models.Issues.objects.filter(project=request.tracer.project, id=issues_id).first()
    form = IssuesModelForm(request, instance=issues_object) 
    return render(request, 'issues_detail.html', {'form': form, 'issues_object': issues_object})

@csrf_exempt
def issues_record(request, project_id, issues_id):
    if request.method == 'GET':
        reply_list = models.IssuesReply.objects.filter(issues_id=issues_id, issues__project=request.tracer.project)
        
        # 将queryset转换为json格式
        data_list = []
        for row in reply_list:
            data = {
                    'id': row.id,
                    'reply_type_text': row.get_reply_type_display(),
                    'content': row.content,
                    'creator': row.creator.username,
                    'datetime': row.create_datetime.strftime("%Y-%m-%d %H:%M"),
                    'parent_id': row.reply_id
            }
            data_list.append(data)

        return JsonResponse({'status': True, 'data': data_list})
    
    form = IssuesReplyModelForm(data=request.POST)
    
    if form.is_valid():
        form.instance.reply_type = 2
        form.instance.issues_id = issues_id
        form.instance.creator = request.tracer.user
        instance = form.save()
        info = {
            'id': instance.id,
            'reply_type_text': instance.get_reply_type_display(),
            'content': instance.content,
            'creator': instance.creator.username,
            'datetime': instance.create_datetime.strftime("%Y-%m-%d %H:%M"),
            'parent_id': instance.reply_id
        }
        
        return JsonResponse({'status': True, 'data': info})
    return JsonResponse({'status': False, 'error': form.errors})