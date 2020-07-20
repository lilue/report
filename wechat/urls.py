from wechat import views
from django.urls import path

urlpatterns = [
    path('', views.handle_wx),
    path('render/', views.render),
    path('getMenu/', views.get_menu_info())
]