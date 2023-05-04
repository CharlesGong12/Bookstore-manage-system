from django.shortcuts import render, redirect
from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from django.db.models import Q
from app01.utils.pagination import Pagination
from app01.utils.form import *


def admin_list(request):
    queryset = models.Admin.objects.all().order_by('group')
    return render(request, 'admin_list.html', {'queryset': queryset})


def admin_add(request):
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, 'title': '新建管理员'})
    else:  # POST
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            # 如果有错，信息不能存储，自然无效
            form.save()
            return redirect('/admin/list/')
        else:
            return render(request, 'change.html', {'form': form, 'title': '新建管理员'})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()  # 默认列表，只有取first才可以取出对象
    if not row_object:
        # 存在性检查时为了防止并发操作
        return render(request, 'error.html', {'error_msg': '该数据不存在'})

    title = '编辑管理员'
    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form, 'title': title})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    else:
        return render(request, 'change.html', {'form': form, 'title': title})


def admin_reset(request, nid):
    # 重置密码

    row_object = models.Admin.objects.filter(id=nid).first()
    title = "重置密码 用户: {}".format(row_object.username)
    if not row_object:
        return render(request, 'error.html', {'error_msg': '操作的对象不存在'})
    if request.method == 'GET':
        form = AdminResetModelForm()  # 不输入instance 不能查看原有密码
        return render(request, 'change.html', {'form': form, 'title': title})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    else:
        return render(request, 'change.html', {'form': form, 'title': title})
