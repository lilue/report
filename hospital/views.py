from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from report import settings
# Create your views here.


@require_http_methods(["GET"])
def home(request):
    menu = [
        {
            'url': 'patient',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '预约挂号',
            'type': 'test1'
        }, {
            'url': 'patient',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '门诊缴费',
            'type': 'test2'
        }, {
            'url': 'patient',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '核酸缴费',
            'type': 'test3'
        }, {
            'url': 'patient',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '个人中心',
            'type': 'test4'
        }, {
            'url': 'patient',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '诊疗卡开卡',
            'type': 'test5'
        }, {
            'url': 'patient',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '核酸报告',
            'type': 'test6'
        }, {
            'url': 'patient',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '缴费记录',
            'type': 'test7'
        }, {
            'url': 'patient',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '电子票夹',
            'type': 'test8'
        }, {
            'url': 'patient',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '联系电话',
            'type': 'test9'
        }
    ]
    return render(request, 'hospital/index.html', {'menu': menu})


@require_http_methods(["GET"])
def patient(request, style):
    return render(request, 'hospital/patient_list.html', {'page': style})


@require_http_methods(["GET"])
def notData(request):
    return render(request, 'hospital/notdata.html')
