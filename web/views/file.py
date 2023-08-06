'''
Author: Misaki
Date: 2023-08-03 15:40:26
LastEditTime: 2023-08-06 17:36:11
LastEditors: Misaki
Description: 
'''

from msilib.schema import File
from winreg import QueryInfoKey
from django.shortcuts import render, redirect
from web import models
from web.forms.file import FileModelForm
from django.http import JsonResponse
from django.forms import model_to_dict
from utils.tencent.cos import credential, delete_file, delete_file_list


def file(request, project_id):
    """文件列表&添加文件夹

    Args:
        request (_type_): _description_
        project_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    # 先获得父级目录
    parent_object = None
    folder_id = request.GET.get('folder', '')
    if folder_id.isdecimal():
        parent_object = models.FileRepository.objects.filter(id=int(folder_id), file_type=2,
                                                             project=request.tracer.project).first()    
    
    # GET请求就是展示页面
    if(request.method == 'GET'):
        form = FileModelForm(request, parent_object)    
        parent = parent_object
        breadcrumb_list = []
        while parent:
            breadcrumb_list.insert(0, model_to_dict(parent, ['id', 'name']))
            parent = parent.parent
        

        # 如果进入了目录, 就把当前项目当前目录的文件夹与文件都获得
        querryset = models.FileRepository.objects.filter(project=request.tracer.project) 
        if parent_object:
            file_object_list = querryset.filter(parent=parent_object).order_by('-file_type')

        # 否则根目录
        else:
            file_object_list = querryset.filter(parent__isnull=True).order_by('-file_type')
        
        
        context = {
            'form': form,
            'file_object_list': file_object_list,
            'breadcrumb_list': breadcrumb_list
        }
        
        return render(request, 'file.html', context=context)
    
    # POST请求，提交页面
    # 新建文件夹 or 编辑文件夹
    fid = request.POST.get('fid', '')
    edit_object = None
    if fid.isdecimal():
        edit_object = models.FileRepository.objects.filter(id=int(fid), 
                                                           file_type=2,
                                                           project=request.tracer.project).first()
    
    if edit_object:
        form = FileModelForm(request, parent_object, data=request.POST, instance=edit_object)
    else:
        form = FileModelForm(request, parent_object, data=request.POST)
    
    if(form.is_valid()):
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def file_delete(request, project_id):
    fid = request.GET.get('fid')
    
    delete_object = models.FileRepository.objects.filter(project=request.tracer.project, id=fid).first()
    
    # cos删除、数据库删除、归还容量

    # 删除文件，归还容量
    if delete_object.file_type == 1:
        request.tracer.project.use_space -= delete_object.file_size
        request.tracer.project.save()
    
    # cos中删除文件
    delete_file(request.tracer.project.bucket, request.tracer.project.region, delete_object.key)
    

# 删除文件夹（找到文件夹下所有的文件->数据库文件删除、cos文件删除、项目已使用空间容量还回去）
    # delete_object
    # 找他下面的 文件和文件夹
    # models.FileRepository.objects.filter(parent=delete_object) # 文件 删除；文件夹 继续向里差

    total_size = 0
    key_list = []

    folder_list = [delete_object, ]
    for folder in folder_list:
        child_list = models.FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by(
            '-file_type')
        for child in child_list:
            if child.file_type == 2:
                folder_list.append(child)
            else:
                # 文件大小汇总
                total_size += child.file_size

                # 删除文件
                key_list.append({"Key": child.key})

    # cos 批量删除文件
    if key_list:
        delete_file_list(request.tracer.project.bucket, request.tracer.project.region, key_list)

    # 归还容量
    if total_size:
        request.tracer.project.use_space -= total_size
        request.tracer.project.save()

    # 删除数据库中的文件
    delete_object.delete()
    return JsonResponse({'status': True})


def cos_credential(request, project_id):
    data_dict = credential(request.tracer.project.bucket, request.tracer.project.region)
    return JsonResponse(data_dict)
    