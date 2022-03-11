from hospital import views
from django.urls import path

urlpatterns = [
    path('home', views.home, name="home"),
    path('patient/<str:style>/', views.patient, name="patient"),
    path('nodata', views.notData, name="nodata")
]
