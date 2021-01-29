from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('config', csrf_exempt(views.Obtain.as_view()), name="getConfig"),
    path('ocr', csrf_exempt(views.CardOcr.as_view()), name="card_ocr"),
]
