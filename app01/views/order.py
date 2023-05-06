from django.shortcuts import render, redirect
from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from django.db.models import Q
from django.db import transaction
from app01.utils.pagination import Pagination
from app01.utils.form import *


def order_list(request):
    queryset = models.Order.objects.all().order_by('state', 'timestamp')
    page_object = Pagination(request, queryset, page_size=8)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
    }
    return render(request, 'order_list.html', context)


def order_add(request):
    if request.method == 'GET':
        form = OrderModelForm()
        return render(request, 'change.html', {'form': form, 'title': '新建订单'})
    else:  # POST
        form = OrderModelForm(data=request.POST)
        if form.is_valid():
            # 如果有效
            # 时间会自动加，需要附加上用户名
            info_dict = request.session.get('info')  # 获取当前用户名
            admin = models.Admin.objects.get(username=info_dict['username'])
            order = form.save(commit=False)
            order.username = admin  # 外键必须关联到一个对象!
            order.save()  # 通过modelform保存到model
            return redirect('/order/list/')
        else:
            # 错误信息附加
            return render(request, 'change.html', {'form': form, 'title': '新建订单'})


def order_cancel(request, nid):
    if models.Order.objects.filter(id=nid, state__gt=1):
        # 说明操作错误，只允许取消未支付的订单
        return redirect('/order/list/')
    models.Order.objects.filter(id=nid).update(state=3)
    return redirect('/order/list/')


def order_delete(request, nid):
    if models.Order.objects.filter(id=nid, state=1):
        # 说明操作错误，不允许删除未支付的订单
        return redirect('/order/list/')
    models.Order.objects.filter(id=nid).delete()
    return redirect('/order/list/')


def order_pay(request, nid):
    if models.Order.objects.filter(id=nid).exclude(state=1).exists():
        # 说明操作错误，只允许支付“未支付”的订单
        return redirect('/order/list/')
    row_object = models.Order.objects.filter(id=nid).first()  # 获取当前订单对象
    info_dict = request.session.get('info')
    username = info_dict['username']  # 获取当前用户名
    txt_isbn = row_object.isbn  # 获取当前isbn
    book_name = models.BookInfo.objects.filter(isbn=txt_isbn).first().name  # 找到该isbn对应的书名
    models.Bill.objects.create(type=2, amount= -row_object.total,
                               description='图书进货付款:《{name}》*{num}'.format(name = book_name,
                                                                                num=row_object.purchase_amount),
                               username=models.Admin.objects.filter(username=username).first())
    balance_object = models.SystemBalance.objects.first()
    if not balance_object:
        models.SystemBalance.objects.create(balance=0)
        balance_object = models.SystemBalance.objects.first()
    origin_balance = balance_object.balance
    models.SystemBalance.objects.all().update(balance=origin_balance - row_object.total)
    models.Order.objects.filter(id=nid).update(state=2)
    return redirect('/order/list/')
