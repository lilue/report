from django.contrib import admin
from .models import User
from django.utils.safestring import mark_safe
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 屏蔽管理界面的添加按钮
    def has_add_permission(self, request):
        return False

    # 显示头像缩略图
    def upload_img(self, obj):
        # print(obj.avatar)
        try:
            img = mark_safe('<img src="%s" width="50px" />' % (obj.avatar,))
        except Exception as e:
            print(str(e))
            img = ''
        # print(img)
        return img

    upload_img.short_description = '微信头像'
    upload_img.allow_tags = True
    empty_value_display = '-empty-'
    list_display = ['nickname', 'username', 'upload_img', 'is_staff']
    list_display_links = ['nickname']
    readonly_fields = ['open_id']
    list_editable = ['is_staff']


admin.site.site_title = "发票管理"
admin.site.site_header = "坡头人民医院发票管理"
