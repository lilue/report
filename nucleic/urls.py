from django.urls import path
from .views import oauth
from nucleic import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('home/<str:pk>', oauth(views.index), name="home-page"),
    path('progress/<str:pk>', views.waitingPay, name="waitPay"),
    path('finsh/<str:pk>', views.complete, name="payment-complete"),
    path('smallticket', views.ticket, name="small-ticket"),
    # path('refunds', views.refund, name="refund"),
    path('unified', views.payment, name="go-pay"),
    # path('checkStatus/<str:pk>', views.print_status, name="check-status"),
    # path('test', views.get_wx_user_info, name="user-info"),
    path('qrcode/<str:pk>/down', views.downQr, name="qrcode"),
    path('callback', csrf_exempt(views.notify), name="notify-url"),
    # path('refund_callback', csrf_exempt(views.refund_notify), name="refund_notify-url"),
    # path('config', views.Obtain.as_view(), name="getConfig"),
]
