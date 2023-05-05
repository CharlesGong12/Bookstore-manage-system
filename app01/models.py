from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


# Create your models here.

class BookInfo(models.Model):
    isbn = models.CharField(verbose_name="ISBN", max_length=13, unique=True)
    name = models.CharField(verbose_name="书名", max_length=50)
    press = models.CharField(verbose_name="出版社", max_length=30, null=True, blank=True)
    author = models.CharField(verbose_name="作者", max_length=60, null=True, blank=True)
    retail_price = models.DecimalField(verbose_name="零售价格", max_digits=10, decimal_places=2, default=0)
    amount = models.IntegerField(verbose_name="库存数量", default=0)


class Admin(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    employee_id = models.CharField(verbose_name='工号', max_length=11, unique=True)
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


class SystemBalance(models.Model):
    # 系统账号余额
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)


class Bill(models.Model):
    type_choices = (
        (1, '收入'),
        (2, '支出')
    )

    timestamp = models.DateTimeField(verbose_name='时间', default=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    username = models.ForeignKey(verbose_name='操作用户', to='Admin', to_field='username', null=True, blank=True,
                                 on_delete=models.SET_NULL, db_column='username')
    # 在 Django 的 ORM 中ForeignKey默认会使用对应模型的主键作为关联字段
    # 因此在数据库中对应的列属性为整型数字（即该模型的主键类型）。还会加上_id标识
    # 会关联的是对象！而不是字段
    # 如果外键使用时，在数据库中使用其他类型的列属性，可以使用模型中的db_column选项来指定具体的列名
    type = models.SmallIntegerField(verbose_name='类型', choices=type_choices)
    amount = models.DecimalField(verbose_name='金额', max_digits=16, decimal_places=2)
    description = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)


class Order(models.Model):
    timestamp = models.DateTimeField(verbose_name='创建时间', default=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    username = models.ForeignKey(verbose_name='操作用户', to='Admin', to_field='username', null=True, blank=True,
                                 on_delete=models.SET_NULL, db_column='username')
    isbn = models.CharField(verbose_name="ISBN", max_length=13)
    purchase_price = models.DecimalField(verbose_name="进货价格", max_digits=8, decimal_places=2, default=0,
                                         validators=[MinValueValidator(0)])
    purchase_amount = models.PositiveIntegerField(verbose_name="进货数量")
    total = models.DecimalField(verbose_name='总金额', max_digits=12, decimal_places=2, default=0)
    state_choice = ((1, '未支付'), (2, '已支付'), (3, '已取消'))
    state = models.SmallIntegerField(verbose_name='订单状态', choices=state_choice, default=1)

    def save(self, *args, **kwargs):
        # 在模型保存时会自动计算这个属性
        self.total = (self.purchase_price * self.purchase_amount)
        super(Order, self).save(*args, **kwargs)
