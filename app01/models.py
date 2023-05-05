from django.db import models


# Create your models here.

class BookInfo(models.Model):
    isbn = models.CharField(verbose_name="ISBN", max_length=13)
    name = models.CharField(verbose_name="书名", max_length=50)
    press = models.CharField(verbose_name="出版社", max_length=30, null=True, blank=True)
    author = models.CharField(verbose_name="作者", max_length=60, null=True, blank=True)
    retail_price = models.DecimalField(verbose_name="零售价格", max_digits=10, decimal_places=2, default=0)
    amount = models.IntegerField(verbose_name="库存数量", default=0)


class Admin(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    employee_id = models.CharField(verbose_name='工号', max_length=11)
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    # 在django中做的约束 建立映射关系
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    group_choices = (
        (1, "超级管理员"),
        (2, "普通管理员"),
    )
    group = models.SmallIntegerField(verbose_name='用户组', choices=group_choices)
