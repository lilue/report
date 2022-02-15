from wechat import views
from django.urls import path

urlpatterns = [
    path('', views.handle_wx),
    path('materials', views.getMaterialsCount),
    path('materialsList/<str:media>/<int:offset>/', views.getMaterialsList),
    path('message', views.getMessageList),
    path('test', views.menu),
    path('getMenu', views.getMenu),
    path('batchget/<int:offset>/', views.getBatchget),
    path('menu', views.createMenu),
    path('demo', views.getJson),
    path('uploadImg', views.uploadImg),
    path('getmaterials/<str:media>', views.getMaterial)
    # path('render/', views.render),
]
