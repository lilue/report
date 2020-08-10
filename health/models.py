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
    erhc_card_no = models.CharField(max_length=200, default='', verbose_name="电子健康码ID")
    empi = models.CharField(max_length=200, default='', verbose_name="主索引ID")
    qr_code = models.CharField(max_length=200, default='', verbose_name="静态二维码")
    is_default = models.CharField(max_length=10, default='0', verbose_name="是否设置为默认卡")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'id_code': self.id_code,
            'erhc_card_no': self.erhc_card_no,
            'empi': self.empi,
            'qr_code': self.qr_code,
            'is_default': self.is_default,
            'user': self.user.openid
        }
