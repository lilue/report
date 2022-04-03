from wechat import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', csrf_exempt(views.handle_wx)),
    path('test', csrf_exempt(views.menu)),
    path('getMenu', csrf_exempt(views.getMenu)),
    path('menu', csrf_exempt(views.createMenu))
    # path('render/', views.render),
]
