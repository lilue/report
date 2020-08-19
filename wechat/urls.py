from wechat import views
from django.urls import path

urlpatterns = [
    path('', views.handle_wx),
    path('menu', views.createMenu)
    # path('render/', views.render),
]
