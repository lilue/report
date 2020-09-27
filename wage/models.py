from django.db import models

# Create your models here.


class Payroll(models.Model):
    idCard = models.CharField(max_length=30, verbose_name='身份证号码')
    random_code = models.CharField(max_length=30, verbose_name='随机验证码')
    content = models.CharField(max_length=255, verbose_name='工资条')
