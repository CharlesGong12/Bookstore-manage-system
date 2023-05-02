from django.db import models


# Create your models here.

class BookInfo(models.Model):
    isbn = models.CharField(verbose_name="ISBN", max_length=13)
    name = models.CharField(verbose_name="书名", max_length=50)
    press = models.CharField(verbose_name="出版社", max_length=30, null=True, blank=True)
    author = models.CharField(verbose_name="作者", max_length=60, null=True, blank=True)
    retail_price = models.DecimalField(verbose_name="零售价格", max_digits=10, decimal_places=2, default=0)
    amount = models.IntegerField(verbose_name="库存数量", default=0)
