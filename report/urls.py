"""report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from report import settings
from hospital import views

urlpatterns = [
    path('MP_verify_mQJFPw6llNu89Htp.txt', views.wx_verify),
    # path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('wx/', include('wechat.urls')),
    path('health/', include('health.urls')),
    path('api/', include('interface.urls')),
    path('auth/', include('authorization.urls')),
    path('website/', include('hospital.urls'))
    # path('menu/', include('makepdf.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
