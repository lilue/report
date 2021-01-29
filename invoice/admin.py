from django.contrib import admin
from .models import Invoice
from django.shortcuts import get_object_or_404, redirect
from django.utils.safestring import mark_safe
# Register your models here.


class TitleKeywordFilter(admin.SimpleListFilter):
    title = '受票方名称'
    parameter_name = 'keyword'
    """
    自定义需要筛选的参数元组
    """
    def lookups(self, request, model_admin):
        return(
            ('first', '查询所有'),
            ('one', '湛江市坡头区人民医院'),
            ('two', '坡头区坡头镇中心卫生院'),
        )

    def queryset(self, request, queryset):
        """
        调用self.value()获取url中的参数，然后筛选所需的queryset
        """
        # print(self.value())
        # print(queryset.filter(purchaser='广东中拓信息技术有限公司'))
        if self.value() == 'one':
            return queryset.filter(purchaser='湛江市坡头区人民医院')
        elif self.value() == 'two':
            return queryset.filter(purchaser='坡头区坡头镇中心卫生院')
        elif self.value() == 'first':
            return queryset
        else:
            return queryset


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    # 屏蔽管理界面的添加按钮
    def has_add_permission(self, request):
        return False

    # 判断是否勾选确认
    def confirm_txt(self, obj):
        if obj.confirm:
            return mark_safe('<text style="color: green;">已确认</text>')
        else:
            dest = '{}confirm/'.format(obj.pk)
            return mark_safe('<a href="{}" style="color:red !important">未确认</a>'.format((dest)))

    confirm_txt.short_description = '是否确认'
    confirm_txt.allow_tags = True

    # 添加是否确认路由
    def get_urls(self):
        """添加一个url，指向实现删除图片功能的方法"""
        from django.conf.urls import url
        urls = [
            url('^(?P<pk>\d+)confirm/?$', self.admin_site.admin_view(self.confirm_btn),
                name='confirm_btn'),
        ]
        return urls + super(InvoiceAdmin, self).get_urls()

    # 函数实现确认发票
    def confirm_btn(self, request, *args, **kwargs):
        obj = get_object_or_404(Invoice, pk=kwargs['pk'])
        print(request.user)
        if not obj.confirm:
            obj.confirm = True
            obj.save()
        path = request.path.split('/')
        path = '/'.join(path[:-2]).strip('')
        return redirect(path)

    def check_purchaser(self, obj):
        judgment = True
        if obj.purchaser != '湛江市坡头区人民医院' and obj.purchaser_number != '12440804456250892W':
            judgment = False
        if obj.purchaser != '坡头区坡头镇中心卫生院' and obj.purchaser_number != '124408047993279516':
            judgment = False
        if judgment:
            return mark_safe('<text>{}</text>')
        else:
            return mark_safe('<text style="color: red;">{}</text>'.format(obj.purchaser))

    check_purchaser.short_description = '受票方名称'
    check_purchaser.allow_tags = True

    list_display = ['number', 'code', 'seller', 'seller_number', 'amount', 'check_purchaser', 'date', 'confirm_txt',
                    'user', 'create_date']
    list_display_links = ['number']
    readonly_fields = ['number', 'code', 'seller', 'seller_number', 'amount', 'purchaser',
                       'purchaser_number', 'date', 'user', 'create_date']
    fields = ('number', 'code', 'seller', 'seller_number', 'amount', 'purchaser', 'purchaser_number', 'date',
              'user', 'create_date', 'confirm')
    list_filter = (TitleKeywordFilter,)
