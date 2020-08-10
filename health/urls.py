from health import views
from django.urls import path


urlpatterns = [
    path('', views.Management.as_view(), name='index'),
    path('user/info', views.get_wx_user_info),
    path('newCard', views.add_card, name='addCard'),
    path('MP_verify_PJRLUusp1NXyuD70.txt', views.wx_verify)
    # path('render/', views.render),
]
