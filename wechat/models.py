from django.db import models

# Create your models here.


class Menu(models.Model):
    class Meta:
        verbose_name = '微信菜单'
        verbose_name_plural = verbose_name
