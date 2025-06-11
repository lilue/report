from django.contrib import admin
from django.urls import reverse
from .models import Payment, QRconfig
from django.utils.safestring import mark_safe
from report import settings
# Register your models here.

# 以前坡头这个界面是打开的，农垦2院被我注释了
# @admin.register(QRconfig)
# class QRconfigAdmin(admin.ModelAdmin):
#     list_display = ['id', 'hospital', 'location', 'itemName', 'price', 'status', 'download_code']
#     fields = ['hospital', 'location', 'itemName', 'price', 'status']
#     list_display_links = ['location']
#
#     def has_delete_permission(self, request, obj=None):
#         if request.user.is_superuser:
#             return True
#         # 禁用删除按钮
#         return False
#
#     def download_code(self, obj):
#         title = '下载二维码'
#         url = reverse('qrcode', kwargs={'pk': obj.pk})
#         # print("url:" + url)
#         # url_path = 'http://' + request.META['HTTP_HOST'] + '/payment/home/' + obj.pk
#         return mark_safe('<a href="{}">{}</a>'.format(url, title))
#
#     download_code.short_description = '下载二维码'
#     download_code.allow_tags = True
#
#
# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'patient', 'number', 'money', 'orderNo', 'transactionID', 'payStatus', 'timeEnd']
#     # fields = ['patient']
#     # readonly_fields = ['id', 'patient', 'number', 'amount', 'orderNo', 'transactionID', 'status', 'notify', 'timeEnd']
#     list_display_links = None
#     list_filter = ['create_time']
#     # date_hierarchy = 'create_time'
#     # list_max_show_all = 50
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.filter(status='2')
#
#     def has_add_permission(self, request):
#         # 禁用添加按钮
#         return False
#
#     def money(self, obj):
#         return obj.amount / 100
#
#     money.short_description = '支付金额'
#     money.allow_tags = True
#
#     def payStatus(self, obj):
#         if obj.status == '1':
#             return '未支付'
#         elif obj.status == '2':
#             return '已支付'
#         elif obj.status == '3':
#             return '已退款'
#         else:
#             return '订单关闭'
#
#     payStatus.short_description = '支付状态'
#     payStatus.allow_tags = True
#
#     def has_delete_permission(self, request, obj=None):
#         # if request.user.is_superuser:
#         #     return True
#         # 禁用删除按钮
#         return False


# admin.site.site_header = settings.SITE_HEADER
# admin.site.site_title = "登录系统后台"
# admin.site.index_title = "后台管理"
