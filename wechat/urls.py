from wechat import views
from django.urls import path

urlpatterns = [
    path('', views.handle_wx),
    path('materials', views.getMaterialsCount),
    path('materialsList', views.getMaterialsList),
    path('message', views.getMessageList),
    path('test', views.menu),
    # path('getMenu', views.getMenu),
    # path('menu', views.createMenu)
    # path('render/', views.render),
]
