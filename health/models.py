from django.db import models

# Create your models here.


class UserProfile(models.Model):
    openid = models.CharField(max_length=32, default='', verbose_name="微信openid")
    nickname = models.CharField(max_length=256, default='', verbose_name="微信昵称")
    head_url = models.CharField(max_length=200, default='', verbose_name="微信头像")

    def __str__(self):
        return self.openid

    def to_dict(self):
        return {
            'id': self.id,
            'openid': self.openid,
            'nickname': self.nickname,
            'head_url': self.head_url,
        }


class UserCard(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT, default='', verbose_name="用户")
    name = models.CharField(max_length=256, default='', verbose_name="姓名")
    id_code = models.CharField(max_length=18, default='', verbose_name="证件号码")
    phone = models.CharField(max_length=11, default='', verbose_name="联系电话")
    erhc_card_no = models.CharField(max_length=200, default='', verbose_name="电子健康码ID")
    empi = models.CharField(max_length=200, default='', verbose_name="主索引ID")
    qr_code = models.CharField(max_length=200, default='', verbose_name="静态二维码")
    medical = models.CharField(max_length=32, default='', verbose_name="诊疗卡号")
    is_untie = models.CharField(max_length=10, default='0', verbose_name="是否解绑，默认创建则绑定，1解绑")
    is_default = models.CharField(max_length=10, default='0', verbose_name="是否设置为默认卡")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'idCard': self.id_code,
            'erhc_card_no': self.erhc_card_no,
            'empi': self.empi,
            'phone': self.phone,
            'qrCodeText': self.qr_code,
            'is_default': self.is_default,
            'is_untie': self.is_untie,
            'medical': self.medical,
            'user': self.user.openid
        }
