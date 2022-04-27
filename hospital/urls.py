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
    path('acidOrder', views.acid_order, name="acid"),
    path('notify_url', csrf_exempt(views.notify), name="notify"),
    path('acid_notify', csrf_exempt(views.acid_notify), name="acid_notify"),
    path('nucleicAcid', oauth(views.acid), name="covid"),
    path('acidResult/<int:pk>', oauth(views.acid_result), name="acidRes"),
    path('acidList', oauth(views.acid_list), name="acidList"),
    path('nodata', oauth(views.notData), name="nodata"),
    path('obtain', csrf_exempt(views.obtain), name="getPayUrl"),
    path('query/<str:order>', csrf_exempt(views.query_pay), name="queryPay"),
    path('microPay', csrf_exempt(views.microPay), name="microPay"),
]
