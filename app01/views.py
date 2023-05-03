from django.shortcuts import render, redirect
from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from django.db.models import Q
from app01.utils.pagination import Pagination


# Create your views here.
class BookInfoModelForm(forms.ModelForm):
    isbn = forms.CharField(label="ISBN", max_length=13,
                           validators=[RegexValidator(
                               r'^(?:ISBN(?:-10)?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$)[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$',
                               'ISBN格式错误'), ])

    class Meta:
        model = models.BookInfo
        fields = ['isbn', 'name', 'press', 'author', 'retail_price', 'amount']  # 可以自己指定 也可以__all__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 调用父类的构造函数
        for name, field in self.fields.items():  # 这个方法可以减少工作量，不需要一个一个加widget
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}
            # if name == '': 特殊指定
            #     continue

    # 校验方法2：钩子函数 去重 不允许添加重复的isbn号书目
    def clean_isbn(self):
        txt_isbn = self.cleaned_data['isbn']
        exist = models.BookInfo.objects.filter(isbn=txt_isbn).exists()
        if not exist:
            return txt_isbn
        else:
            raise ValidationError('该ISBN对应书目信息已存在')


class BookEditInfoModelForm(forms.ModelForm):
    isbn = forms.CharField(disabled=True, label="ISBN")  # 不允许修改isbn号
    amount = forms.IntegerField(disabled=True, label='库存数量')  # 创建后即不允许修改库存数量，只能通过进出货修改

    class Meta:
        model = models.BookInfo
        fields = ['isbn', 'name', 'press', 'author', 'retail_price', 'amount']  # 可以自己指定 也可以__all__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 调用父类的构造函数
        for name, field in self.fields.items():  # 这个方法可以减少工作量，不需要一个一个加widget
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}
            # if name == '': 特殊指定
            #     continue


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
    row_object = models.BookInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = BookEditInfoModelForm(instance=row_object)
        # 使用instance属性，这种方式可以实现填写默认值，相当于把value属性全部设置。还有一个功能是能找到更新的位置
        return render(request, 'book_edit.html', {'form': form})
    else:
        form = BookEditInfoModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/book/list/')
        else:
            return render(request, 'book_edit.html', {'form': form})


def book_delete(request, nid):
    models.BookInfo.objects.filter(id=nid).delete()
    return redirect('/book/list/')


def book_sale(request, nid):
    pass
