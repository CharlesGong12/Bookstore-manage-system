from django.shortcuts import render, redirect
from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from django.db.models import Q
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
        return render(request, 'change.html', {'form': form,'title':title})
    else:
        form = BookEditInfoModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/book/list/')
        else:
            return render(request, 'change.html', {'form': form,'title':title})


def book_delete(request, nid):
    models.BookInfo.objects.filter(id=nid).delete()
    return redirect('/book/list/')


def book_sale(request, nid):
    pass
