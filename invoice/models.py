from django.db import models
from authorization.models import User
from django.utils import timezone
from django.contrib.auth.models import User as AUser
# Create your models here.


class Invoice(models.Model):
    number = models.CharField(max_length=32, verbose_name="发票号码", default='')
    code = models.CharField(max_length=32, verbose_name="发票代码", default='')
    amount = models.CharField(max_length=32, verbose_name="发票金额", default='')
    date = models.CharField(max_length=20, verbose_name="开票日期", default='')
    confirm = models.BooleanField(default=False, verbose_name="是否确认")
    confirm_date = models.CharField(max_length=20, verbose_name="修改状态日期", blank=True, null=True, default='')
    confirm_user = models.CharField(max_length=20, verbose_name="修改状态用户", blank=True, null=True, default='')
    user = models.CharField(max_length=20, verbose_name="录入用户", blank=True, null=True, default='')
    create_date = models.DateField(default=timezone.now, verbose_name="创建时间")
    update_data = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    class Meta:
        verbose_name = '发票列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

    def to_dict(self):
        return {
            'id': self.pk,
            'number': self.number,
            'code': self.code,
            'amount': self.amount,
            'date': self.date,
            'user': self.user,
            'confirm': self.confirm,
            'create_date': self.create_date
        }


class InvoiceLog(models.Model):
    content = models.CharField(max_length=256, verbose_name="操作内容")
    edit_date = models.DateField(default=timezone.now, verbose_name="修改时间")
    edit_user = models.ForeignKey(AUser, on_delete=models.PROTECT, default='', verbose_name='修改用户')

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pk
