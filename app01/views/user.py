from django.shortcuts import render, redirect
from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from django.db.models import Q
from app01.utils.pagination import Pagination
from app01.utils.form import *


#  编辑自己的个人信息的入口(不能编辑别人) 为更新自己的session信息,编辑后需要重新登录
def user_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()  # 默认列表，只有取first才可以取出对象
    if not row_object:
        # 存在性检查时为了防止并发操作
        return render(request, 'error.html', {'error_msg': '该数据不存在'})
    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/logout/')
    else:
        return render(request, 'user_edit.html', {'form': form})
