from health import views
from django.urls import path
from .views import oauth


urlpatterns = [
    path('', views.Management.as_view(), name='index'),
    path('user/info', views.get_wx_user_info),
    path('card', views.health.as_view(), name='card'),
    path('personal/<int:no>/', views.bind_success, name='suc'),
    path('untie/', views.untie_health, name='untie'),
    path('health_list/', views.health_card_list, name='cardList'),
    path('MP_verify_PJRLUusp1NXyuD70.txt', views.wx_verify),
    # path('render/', views.render),
]
