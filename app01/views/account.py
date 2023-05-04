from django.shortcuts import render, redirect
from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from django.db.models import Q
from app01.utils.pagination import Pagination
from app01.utils.form import *


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    # POST提交
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 表单有效，需要后端自行检查用户名密码是否正确(是否存在于数据库)
        #  cleaned_data : {'username': 'wupeiqi', 'password': '5e5c3bad7eb35cba3638e145c830c35f'}
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()  # 去数据库找这条数据
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中,其同时作为键，把相应数据存储到后端的session中
        request.session["info"] = {'id': admin_object.id, 'username': admin_object.username,'group':admin_object.group}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/book/list/")

    # 若输入表单无效，form携带错误信息返回登录页面
    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()  # 清除session中的信息 下次登录cookie无法找到有效session，必须重新登录
    return redirect('/login/')  # 退出到登录页面
