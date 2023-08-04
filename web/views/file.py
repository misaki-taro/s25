'''
Author: Misaki
Date: 2023-08-03 15:40:26
LastEditTime: 2023-08-04 16:14:05
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
    
    delete_object.delete()
    
    return JsonResponse({'status': True})