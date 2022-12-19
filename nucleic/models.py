from django.db import models
import uuid
from django.utils import timezone
# Create your models here.


class QRconfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    hospital = models.CharField(max_length=120, verbose_name="医院名称")
    location = models.CharField(max_length=120, verbose_name="采样地点")
    itemName = models.CharField(max_length=120, verbose_name="项目名称")
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=True, blank=True, verbose_name="项目单价")
    status = models.BooleanField(default=True, verbose_name='是否启用二维码')
    path_url = models.CharField(max_length=200, blank=True, verbose_name='链接地址')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', help_text='创建时间')

    class Meta:
        verbose_name = '收费金额配置'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

    def __str__(self):
        return self.location

    def to_dict(self):
        return {
            'id': self.id,
            'hospital': self.hospital,
            'location': self.location,
            'itemName': self.itemName,
            'price': self.price
        }


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    patient = models.CharField(max_length=120, blank=True, null=True, verbose_name="就诊人")
    idcard = models.CharField(max_length=20, blank=True, null=True, verbose_name="证件号码")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="联系电话")
    number = models.CharField(max_length=5, blank=True, null=True, verbose_name="就诊人数")
    amount = models.BigIntegerField(default=0, blank=True, verbose_name="收费单总金额")
    qr = models.ForeignKey(QRconfig, on_delete=models.PROTECT, verbose_name="支付场景二维码")
    orderNo = models.CharField(max_length=32, blank=True, unique=True, verbose_name="微信支付商户单号")
    transactionID = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name="微信支付交易单号")
    prepayId = models.CharField(max_length=100, blank=True, null=True, verbose_name="预支付交易会话标识")
    preTime = models.CharField(max_length=100, blank=True, null=True, verbose_name="统一下单时间戳")
    preNonce = models.CharField(max_length=100, blank=True, null=True, verbose_name="统一下单随机字符串")
    paySign = models.CharField(max_length=200, blank=True, null=True, verbose_name="支付签名")
    openid = models.CharField(max_length=50, blank=True, null=True, verbose_name="缴费的微信openid")
    status = models.CharField(max_length=2, default='1', verbose_name="支付状态")
    printf = models.CharField(max_length=2, default='0', verbose_name="打印标志")
    expDate = models.DateTimeField(blank=True, null=True, verbose_name="过期时间")
    timeEnd = models.CharField(default='', max_length=50, blank=True, null=True, verbose_name="支付完成时间")
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    print_time = models.DateTimeField(default=None, blank=True, null=True, verbose_name='打印时间', help_text='打印时间')

    class Meta:
        verbose_name = '支付订单列表'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

    def __str__(self):
        return self.orderNo

