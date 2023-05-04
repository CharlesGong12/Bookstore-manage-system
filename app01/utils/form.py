from django.core.validators import RegexValidator, ValidationError
from app01 import models
from django import forms
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app01.utils.encrypt import md5


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


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)  # 加入这个属性使得密码不会被清空
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password',
                  'employee_id', 'name', 'age', 'gender', 'group']

        widgets = {
            'password': forms.PasswordInput(render_value=True)  # 这种类型设置使得生成的标签对于输入不可见
        }

    def clean_username(self):
        txt_username = self.cleaned_data['username']
        exist = models.Admin.objects.filter(username=txt_username).exists()
        if not exist:
            return txt_username
        else:
            raise ValidationError('用户名已存在')

    def clean_employee_id(self):
        txt_employee_id = self.cleaned_data['employee_id']
        exist = models.Admin.objects.filter(employee_id=txt_employee_id).exists()
        if not exist:
            return txt_employee_id
        else:
            raise ValidationError('工号已存在')

    def clean_password(self):
        # 钩子函数 最后存储到数据库的是经过此函数处理的值(经过clean方法) 可用于校验
        # self.cleaned_data 可以用于获取用户输入到表单中的值
        password = self.cleaned_data.get('password')
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')  # 程序会根据field中的顺序调用钩子函数处理，则此时password已经加密
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != password:
            raise ValidationError('前后输入密码不一致')  # 数据不会递交，而错误信息会存储于errors中
        else:
            return confirm


class AdminEditModelForm(BootStrapModelForm):
    # 不允许编辑密码 用户组
    group_choices = (
        (1, "超级管理员"),
        (2, "普通管理员"),
    )
    group = forms.ChoiceField(label='用户组', choices=group_choices, disabled=True)

    class Meta:
        model = models.Admin
        fields = ['username', 'employee_id', 'name', 'age', 'gender', 'group']

    def clean_username(self):
        txt_username = self.cleaned_data['username']
        exist = models.Admin.objects.exclude(id=self.instance.pk).filter(username=txt_username).exists()
        # 排除当前编辑的对象，考察手机号是否存在
        # self.instance可以获得当前编辑的对象
        if not exist:
            return txt_username
        else:
            raise ValidationError('用户名已存在')

    def clean_employee_id(self):
        txt_employee_id = self.cleaned_data['employee_id']
        exist = models.Admin.objects.exclude(id=self.instance.pk).filter(employee_id=txt_employee_id).exists()
        # 排除当前编辑的对象，考察手机号是否存在
        # self.instance可以获得当前编辑的对象
        if not exist:
            return txt_employee_id
        else:
            raise ValidationError('工号已存在')


class AdminResetModelForm(BootStrapModelForm):
    password = forms.CharField(label='新密码', widget=forms.PasswordInput(render_value=True))
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)  # 加入这个属性使得密码不会被清空
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']

        widgets = {
            'password': forms.PasswordInput(render_value=True)  # 这种类型设置使得生成的标签对于输入不可见
        }

    def clean_password(self):
        # 钩子函数 最后存储到数据库的是经过此函数处理的值(经过clean方法) 可用于校验
        # self.cleaned_data 可以用于获取用户输入到表单中的值
        password = self.cleaned_data.get('password')
        md5_pwd = md5(password)
        if models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists():
            raise ValidationError('新密码不能与原密码相同')
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')  # 程序会根据field中的顺序调用钩子函数处理，则此时password已经加密
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != password:
            raise ValidationError('前后输入密码不一致')  # 数据不会递交，而错误信息会存储于errors中
        else:
            return confirm


# 校验适合用Form, 因为并不需要与model关联
class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

