from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from app01.utils.bootstrap import BootStrapModelForm


# Create your views here.
class BookInfoModelForm(BootStrapModelForm):
    isbn = forms.CharField(label="ISBN", max_length=13,
                           validators=[RegexValidator(
                               r'^(?:ISBN(?:-10)?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$)[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$',
                               'ISBN格式错误'), ])

    class Meta:
        model = models.BookInfo
        fields = ['isbn', 'name', 'press', 'author', 'retail_price', 'amount']  # 可以自己指定 也可以__all__

    # 校验方法2：钩子函数 去重 不允许添加重复的isbn号书目
    def clean_isbn(self):
        txt_isbn = self.cleaned_data['isbn']
        exist = models.BookInfo.objects.filter(isbn=txt_isbn).exists()
        if not exist:
            return txt_isbn
        else:
            raise ValidationError('该ISBN对应书目信息已存在')


class BookEditInfoModelForm(BootStrapModelForm):
    isbn = forms.CharField(disabled=True, label="ISBN")  # 不允许修改isbn号
    amount = forms.IntegerField(disabled=True, label='库存数量')  # 创建后即不允许修改库存数量，只能通过进出货修改

    class Meta:
        model = models.BookInfo
        fields = ['isbn', 'name', 'press', 'author', 'retail_price', 'amount']  # 可以自己指定 也可以__all__
