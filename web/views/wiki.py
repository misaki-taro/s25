'''
Author: Misaki
Date: 2023-07-28 23:38:37
LastEditTime: 2023-07-31 12:25:39
LastEditors: Misaki
Description: 
'''
from django.shortcuts import render, redirect
from web.forms.wiki import WikiModelForm
from django.http import JsonResponse
from django.urls import reverse
from web import models
from utils.tencent.cos import upload_file
from utils.encrypt import uid
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin

def wiki(request, project_id):
    # wiki 首页
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'wiki.html')
    
    wiki_object = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()
    return render(request, 'wiki.html', {'wiki_object': wiki_object})

def wiki_add(request, project_id):
    # 展示页面
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'wiki_form.html', {'form': form})
    
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        # 判断用户是否已经选择父文章
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        
        form.instance.project = request.tracer.project
        form.save()
        url = reverse('web:manage:wiki_add', kwargs={'project_id': project_id})
        return redirect(url)

    return render(request, 'wiki_form.html', {'form': form})

def catalog(request, project_id):
    # 获取该项目的所有文章
    data = models.Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id').order_by('depth', 'id')
    print(data)
    
    # Json形式返回给ajax 
    return JsonResponse({'status':True, 'data': list(data)})

def wiki_delete(request, project_id, wiki_id):
    wiki_object = models.Wiki.objects.filter(project=request.tracer.project, id=wiki_id).delete()
    url = reverse('web:manage:wiki', kwargs={'project_id': project_id})
    return redirect(url)

def wiki_edit(request, project_id, wiki_id):
    wiki_object = models.Wiki.objects.filter(project=request.tracer.project, id=wiki_id).first()
    # 找不到相应的wiki直接跳转到wiki首页
    if not wiki_object:
        url = reverse('web:manage:wiki', kwargs={'project_id': project_id})
        return redirect(url)
    
    # 展示默认信息 (GET请求)
    if request.method == 'GET':
        form = WikiModelForm(request, instance=wiki_object)
        return render(request, 'wiki_form.html', {'form': form})
        # url = reverse('web:manage:wiki', kwargs={'project_id': project_id}) + '?wiki_id={0}'.format(wiki_id)
        # return redirect(url)
    
    # 修改编辑wiki (POST请求)
    form = WikiModelForm(request, data=request.POST, instance=wiki_object)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth += 1
        else:
            form.instance.path = 1
        form.save()
        url = reverse('web:manage:wiki', 
                      kwargs={'project_id': project_id}) + '?wiki_id={0}'.format(wiki_id)

        return redirect(url)

@csrf_exempt
@xframe_options_sameorigin
def wiki_upload(request, project_id):
    """ markdown插件上传图片 """
    result = {
        'success': 0,
        'message': None,
        'url': None
    }

    image_object = request.FILES.get('editormd-image-file')
    if not image_object:
        result['message'] = "文件不存在"
        return JsonResponse(result)
    
    ext = image_object.name.rsplit('.')[-1]
    key = '{}.{}'.format(uid(request.tracer.user.mobile_phone), ext)
    bucket = request.tracer.project.bucket
    region = request.tracer.project.region
    
    image_url = upload_file(bucket, region, image_object, key)
    
    result['success'] = 1
    result['url'] = image_url

    print(result)
    
    return JsonResponse(result)
    

    