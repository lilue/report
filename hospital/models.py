from django.db import models
from health.models import UserProfile
from django.utils import timezone
# Create your models here.


class Medical(models.Model):
    name = models.CharField(max_length=20,  default='', verbose_name="姓名")
    idCard = models.CharField(max_length=18, default='', verbose_name="身份证号")
    cardId = models.CharField(max_length=50, default='', verbose_name="诊疗卡号")
    patientId = models.CharField(max_length=50, default='', verbose_name="唯一编号")
    sex = models.CharField(max_length=5, default='', verbose_name="性别")
    birth_dat = models.CharField(max_length=20, default='', verbose_name="生日")
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '诊疗卡关联列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Recipe(models.Model):
    c_list = models.CharField(max_length=200, default='', verbose_name="处方列表，字符串形式，以,隔开")
    patientId = models.CharField(max_length=50, default='', verbose_name="唯一编号")
    change = models.TextField(default='[]', verbose_name="费用明细, json.dumps() 后存入")
    therapy = models.TextField(default='[]', verbose_name="治疗项目, json.dumps() 后存入")
    recipe_sum = models.CharField(max_length=100, default='0', null=True, blank=True, verbose_name="处方金额")
    status = models.CharField(max_length=5, default='1', verbose_name="处方状态")

    class Meta:
        verbose_name = '处方保存'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.c_list


class Payment(models.Model):
    orderNo = models.CharField(max_length=32, blank=True, unique=True, verbose_name="微信支付订单号与电子票据业务单号")
    transactionID = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name="微信支付订单号")
    prepayId = models.CharField(max_length=100, blank=True, null=True, verbose_name="预支付交易会话标识")
    preTime = models.CharField(max_length=100, blank=True, null=True, verbose_name="统一下单时间戳")
    preNonce = models.CharField(max_length=100, blank=True, null=True, verbose_name="统一下单随机字符串")
    paySign = models.CharField(max_length=200, blank=True, null=True, verbose_name="支付签名")
    openid = models.CharField(max_length=50, blank=True, null=True, verbose_name="缴费的微信openid")
    status = models.CharField(max_length=2, default='1', verbose_name="支付状态")
    notify = models.CharField(max_length=2, default='0', verbose_name="通知状态")
    expDate = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="过期时间")
    timeEnd = models.CharField(default='', max_length=50, blank=True, null=True, verbose_name="支付完成时间")
    recipe = models.ForeignKey(Recipe, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="订单所关联的处方")

    class Meta:
        verbose_name = '订单列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.orderNo
