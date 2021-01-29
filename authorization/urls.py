from django.urls import path
from authorization import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('test', csrf_exempt(views.test_session)),
    path('invoice', csrf_exempt(views.UserView.as_view())),
    path('authorize', csrf_exempt(views.authorize), name='authorize'),
    path('logout', csrf_exempt(views.logout), name='logout')
]