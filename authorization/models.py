from django.db import models

# Create your models here.


class User(models.Model):
    open_id = models.CharField(max_length=32, unique=True, verbose_name="用户openid")
    nickname = models.CharField(max_length=256, verbose_name="用户微信昵称")
    avatar = models.CharField(max_length=256, default='', verbose_name="用户微信头像")
    username = models.CharField(max_length=256, verbose_name="用户姓名", blank=True, null=True, default='')
    is_staff = models.BooleanField(default=False, verbose_name="是否职工")

    class Meta:
        verbose_name = '小程序用户列表'
        verbose_name_plural = '小程序用户列表'

    def __str__(self):
        return self.nickname

    def to_dict(self):
        return {
            'open_id': self.open_id,
            'nickname': self.nickname,
            'username': self.username,
            'is_staff': self.is_staff
        }
