from makepdf import views
from django.urls import path


urlpatterns = [
    path('setMenu/', views.createMenu),
    path('getMenu/', views.getMenu),
    path('getbatchget/', views.get_batchget),
]