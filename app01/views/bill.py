from django.shortcuts import render, redirect
from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from django.db.models import Q
from app01.utils.pagination import Pagination
from app01.utils.form import *


def bill_list(request):
    queryset = models.Bill.objects.all().order_by('-timestamp')
    page_object = Pagination(request, queryset, page_size=8)
    balance_obj = models.SystemBalance.objects.first()
    if balance_obj:
        balance = balance_obj.balance
    else:
        balance = '--'
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
        'balance': balance,
    }
    return render(request, 'bill_list.html', context)


def bill_add(request):
    if request.method == 'GET':
        form = BillModelForm()
        return render(request, 'change.html', {'form': form, 'title': '新建账单'})
    else:  # POST
        form = BillModelForm(data=request.POST)
        balance_object = models.SystemBalance.objects.first()
        if not balance_object:
            models.SystemBalance.objects.create(balance=0)
            balance_object = models.SystemBalance.objects.first()
        if form.is_valid():
            # 如果有效
            # 时间会自动加，需要附加上用户名
            info_dict = request.session.get('info')  # 获取当前用户名
            admin = models.Admin.objects.get(username=info_dict['username'])
            bill = form.save(commit=False)
            bill.username = admin  # 外键必须关联到一个对象!
            bill.save()
            balance_object.balance += form.cleaned_data['amount']
            balance_object.save()
            return redirect('/bill/list/')
        else:
            # 错误信息附加
            return render(request, 'change.html', {'form': form, 'title': '新建账单'})


def bill_delete(request, nid):
    models.Bill.objects.filter(id=nid).delete()
    return redirect('/bill/list/')
