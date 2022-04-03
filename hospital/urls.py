from hospital import views
from django.urls import path
from health.views import oauth
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('home', oauth(views.home), name="home"),
    path('patient/<str:style>/', oauth(views.patient), name="patient"),
    path('addMedical', views.addMedical, name="addMedical"),
    path('expense/<int:pk>', oauth(views.cost), name="expense"),
    path('place', views.unified_order, name="place"),
    path('notify_url', csrf_exempt(views.notify), name="notify"),
    path('nodata', oauth(views.notData), name="nodata")
]
