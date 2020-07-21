from makepdf import views
from django.urls import path


urlpatterns = [
    path('setMenu/', views.get_menu_info())
]