from django.shortcuts import render, redirect
from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from django.db.models import Q
from django.db import transaction
from app01.utils.pagination import Pagination
from app01.utils.form import *


def book_list(request):
    search_data = request.GET.get('query', '')
    if search_data:
        queryset = models.BookInfo.objects.filter(
            Q(isbn__contains=search_data) | Q(name__contains=search_data) | Q(author__contains=search_data)) \
            .order_by('name')
    else:
        queryset = models.BookInfo.objects.all().order_by('name')
    page_object = Pagination(request, queryset, page_size=8)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
        "search_data": search_data,
    }
    return render(request, 'book_list.html', context)


def book_add(request):
    '''
    待完善
    这个函数用户初始化书籍信息，可以定义库存
    我希望初始化时候定义的库存可以加入到进出货账单上去，便于最后记录
    :param request:
    :return:
    '''
    if request.method == 'GET':
        form = BookInfoModelForm()
        return render(request, 'book_add.html', {'form': form})
    else:
        form = BookInfoModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/book/list/')
        else:
            return render(request, 'book_add.html', {'form': form})


def book_edit(request, nid):
    title = '编辑图书信息'
    row_object = models.BookInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = BookEditInfoModelForm(instance=row_object)
        # 使用instance属性，这种方式可以实现填写默认值，相当于把value属性全部设置。还有一个功能是能找到更新的位置
        return render(request, 'change.html', {'form': form, 'title': title})
    else:
        form = BookEditInfoModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/book/list/')
        else:
            return render(request, 'change.html', {'form': form, 'title': title})


def book_delete(request, nid):
    models.BookInfo.objects.filter(id=nid).delete()
    return redirect('/book/list/')


def book_sale(request, nid):
    title = '图书出售'
    row_object = models.BookInfo.objects.filter(id=nid).first()
    info_dict = request.session.get('info')
    username = info_dict['username']
    if request.method == 'GET':
        form = BookSaleModelForm(instance=row_object)
        # 使用instance属性，这种方式可以实现填写默认值，相当于把value属性全部设置。还有一个功能是能找到更新的位置
        return render(request, 'change.html', {'form': form, 'title': title})
    else:
        remain_amount = row_object.amount
        form = BookSaleModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            with transaction.atomic():
                # 更新库存数量
                # remain_amount = row_object.amount 放在这里就会和sale_amount相同
                sale_amount = form.cleaned_data['sale_amount']
                models.BookInfo.objects.filter(id=nid).update(amount=remain_amount - sale_amount)

                # 创建账单
                amount_type = 1  # 1表示收入
                amount = row_object.retail_price * sale_amount  # 此处amount是本次销售额
                models.Bill.objects.create(type=amount_type, amount=amount,
                                           description='图书出售:《{name}》*{num}'.format(name=form.cleaned_data['name'],
                                                                                      num=sale_amount),
                                           username=models.Admin.objects.filter(username=username).first())

                # 更新余额
                balance_object = models.SystemBalance.objects.first()
                if not balance_object:
                    models.SystemBalance.objects.create(balance=0)
                    balance_object = models.SystemBalance.objects.first()
                origin_balance = balance_object.balance
                models.SystemBalance.objects.all().update(balance=origin_balance + amount)

                return redirect('/book/list/')
        else:
            return render(request, 'change.html', {'form': form, 'title': title})
