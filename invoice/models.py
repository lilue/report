from django.db import models
from authorization.models import User
from django.utils import timezone
# Create your models here.


class Invoice(models.Model):
    number = models.CharField(max_length=32, verbose_name="发票号码", unique=True)
    code = models.CharField(max_length=32, verbose_name="发票代码", default='')
    seller = models.CharField(max_length=256, verbose_name="销售方名称", default='')
    seller_number = models.CharField(max_length=32, default='', verbose_name="销售方税号")
    amount = models.CharField(max_length=32, verbose_name="发票金额", default='')
    purchaser = models.CharField(max_length=256, verbose_name="受票方名称", default='')
    purchaser_number = models.CharField(max_length=32, default='', verbose_name="受票方税号")
    date = models.CharField(max_length=20, verbose_name="开票日期", default='')
    confirm = models.BooleanField(default=False, verbose_name="是否确认")
    user = models.ForeignKey(User, on_delete=models.PROTECT, default='', verbose_name='提交人')
    create_date = models.DateField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        verbose_name = '发票列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.number

    def to_dict(self):
        if self.user.username:
            name = self.user.username
        else:
            name = self.user.nickname
        return {
            'id': self.pk,
            'number': self.number,
            'code': self.code,
            'seller': self.seller,
            'seller_number': self.seller_number,
            'amount': self.amount,
            'purchaser': self.purchaser,
            'purchaser_number': self.purchaser_number,
            'date': self.date,
            'user': name,
            'confirm': self.confirm,
            'create_date': self.create_date
        }
