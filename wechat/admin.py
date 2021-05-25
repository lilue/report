from django.contrib import admin
from .models import Menu
from .views import menu

# Register your models here.


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return menu(request)
