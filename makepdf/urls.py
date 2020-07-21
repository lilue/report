from makepdf import views
from django.urls import path


urlpatterns = [
    path('getMenu/', views.get_menu_info())
]