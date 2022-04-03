import json
import random
import string
import time
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from report import settings
from utils.front import post_ask
from .models import Medical, Recipe, Payment
from health.models import UserProfile
from wechatpy import WeChatPay
from datetime import datetime, timedelta


# Create your views here.


def wx_verify(request):
    return HttpResponse('mQJFPw6llNu89Htp')


@require_http_methods(["GET"])
def home(request):
    menu = [
        {
            'url': 'develop',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '预约挂号',
            'type': 'test1'
        }, {
            'url': '/website/patient/expense',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '门诊缴费',
            'type': 'expense'
        }, {
            'url': '/website/patient/test3',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '核酸缴费',
            'type': 'test3'
        }, {
            'url': '/website/patient/test4',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '个人中心',
            'type': 'test4'
        }, {
            'url': '/website/patient/test5',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '诊疗卡开卡',
            'type': 'test5'
        }, {
            'url': '/website/patient/test6',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '核酸报告',
            'type': 'test6'
        }, {
            'url': '/website/patient/test7',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '缴费记录',
            'type': 'test7'
        }, {
            'url': '/website/patient/test8',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '电子票夹',
            'type': 'test8'
        }, {
            'url': '/website/patient/test9',
            'icon': settings.STATIC_URL + '/hospital/img/favicon.png',
            'name': '联系电话',
            'type': 'test9'
        }
    ]
    return render(request, 'hospital/index.html', {'menu': menu})


@require_http_methods(["POST"])
def addMedical(request):
    post_body = request.POST
    param = {'name': post_body['name'].strip(), 'sfzh': post_body['idCard'].strip(),
             'cardid': post_body['cardId'].strip()}
    splice_str = param['sfzh'] + param['cardid']
    response = post_ask('/api/pay/GetUserInfo', param, splice_str)
    if response['Tag'] == 1 or response['Tag'] == '1':
        result = response['Result']
        user_info = request.session.get('user')
        try:
            user_pro = UserProfile.objects.get(openid=user_info['openid'])
        except UserProfile.DoesNotExist:
            user_pro = None
            return JsonResponse({'message': '微信未登录'}, safe=False)
        try:
            medical = Medical.objects.get(idCard=result['idcard_chr'])
            if medical.user:
                return JsonResponse({'message': '诊疗卡已被绑定'}, safe=False)
            else:
                medical.user = user_pro
                medical.save()
                return JsonResponse({'message': 'success'}, safe=False)
        except Medical.DoesNotExist:
            Medical.objects.create(name=result['name_vchr'], idCard=result['idcard_chr'],
                                   cardId=result['patientcardid_chr'], patientId=result['patientid_chr'],
                                   sex=result['sex_chr'], birth_dat=result['birth_dat'], user=user_pro)
    else:
        return JsonResponse({'message': response['Message']}, safe=False)


@require_http_methods(["GET"])
def patient(request, style):
    user_info = request.session.get('user')
    querySet = Medical.objects.filter(user__openid=user_info['openid'])
    return render(request, 'hospital/patient_list.html', {'page': style, 'querySet': querySet})


@require_http_methods(['GET'])
def cost(request, pk):
    user_info = request.session.get('user')
    money = 0
    try:
        medical = Medical.objects.get(user__openid=user_info['openid'], id=pk)
    except Medical.DoesNotExist:
        return render(request, 'hospital/notdata.html')
    response = post_ask('/api/pay/GetFymxList', {'patientid': medical.patientId}, medical.patientId)
    if response['Tag'] == 1 or response['Tag'] == '1':
        result = response['Result']
        cf_list = ','.join(result['cflist'])
        try:
            recipe = Recipe.objects.get(c_list=cf_list, status='1')
        except Recipe.DoesNotExist:
            for item in result['fymxlist']:
                money = int(money + (float(item['summoney']) * 100))
            for item in result['zlxmlist']:
                money = int(money + (float(item['totalmny_dec']) * 100))
            recipe = Recipe.objects.create(c_list=cf_list, change=json.dumps(result['fymxlist']),
                                           therapy=json.dumps(result['zlxmlist']), patientId=medical.patientId,
                                           recipe_sum=money, status='1')
        therapy_data = json.loads(recipe.therapy)
        change_data = json.loads(recipe.change)
        amount = int(recipe.recipe_sum) / 100
        return render(request, 'hospital/expense.html', {'therapy_data': therapy_data, 'change_data': change_data,
                                                         'amount': amount, 'order': recipe.c_list})
    else:
        return render(request, 'hospital/notdata.html')


@require_http_methods(["GET"])
def notData(request):
    return render(request, 'hospital/notdata.html')


@require_http_methods("POST")
def unified_order(request):
    order = request.POST.get('order')
    user_info = request.session.get('user')['openid']
    try:
        recipe = Recipe.objects.get(c_list=order, status='1')
        querySet = recipe.payment_set.filter(status='1', openid=user_info).order_by('-id')[:1]
        if querySet.exists():
            nowTime = datetime.now()
            pay_order = querySet[0]
            minutes = 10  # 统一下单签名有效期为120分钟，这里设置90分钟重新获取
            if nowTime - pay_order.expDate < timedelta(minutes=minutes):
                if pay_order.status != '1':
                    response = {'retcode': 1, 'msg': '订单不是待支付状态，请稍等重试。'}
                    return JsonResponse(data=response, safe=False)
                payments = {
                    "appid": settings.APP_ID,
                    "timestamp": int(pay_order.preTime),
                    "nonce_str": pay_order.preNonce,
                    "prepay_id": pay_order.prepayId,
                    "paySign": pay_order.paySign
                }
                response = {'retcode': 0, 'data': payments}
                return JsonResponse(data=response, safe=False)
            else:
                # 如果 统一下单时间超过 90 分钟，且状态是 1 ，把这条记录状态改为 0， 关闭订单
                if pay_order.status == '1':
                    close_order(pay_order.orderNo)      # 调用api关闭订单，并修改数据库状态
        if recipe.status == '1':
            order_no = ''.join(random.sample(string.ascii_letters + string.digits, 16))
            description = "门诊缴费"
            # order_amount = int(recipe.recipe_sum)   # 参数单位为分，不能带小数点
            order_amount = 1
            pay = WeChatPay(appid=settings.WECHAT_PAY['APPID'], mch_id=settings.WECHAT_PAY['MCHID'],
                            api_key=settings.WECHAT_PAY['APIKEY'], sandbox=settings.WECHAT_PAY['SANDBOX'])
            result = pay.order.create(trade_type=settings.WECHAT_PAY['TYPE'], body=description, total_fee=order_amount,
                                      notify_url=settings.WECHAT_PAY['NOTIFY'] + '/website/notify_url',
                                      out_trade_no=order_no, user_id=user_info)
            timestamp = int(time.time())
            if result['result_code'] == "SUCCESS" and result['return_code'] == "SUCCESS":
                # paySign = pay.jsapi.get_jsapi_signature(prepay_id=result['prepay_id'], timestamp=timestamp,
                #                                         nonce_str=result['nonce_str'])
                params = pay.jsapi.get_jsapi_params(prepay_id=result['prepay_id'], timestamp=timestamp,
                                                    nonce_str=result['nonce_str'], jssdk=True)
                pay_order = Payment.objects.create(
                    orderNo=order_no,
                    paySign=params['paySign'],
                    preNonce=params['nonceStr'],
                    prepayId=params['package'],
                    preTime=params['timestamp'],
                    openid=user_info,
                    recipe=recipe
                )
                payments = {
                    "appid": settings.APP_ID,
                    "timestamp": pay_order.preTime,
                    "nonce_str": pay_order.preNonce,
                    "prepay_id": pay_order.prepayId,
                    "paySign": pay_order.paySign
                }
                response = {'retcode': 0, 'data': payments}
                return JsonResponse(response, safe=False)
            else:
                response = {'retcode': 1, 'msg': '下单失败'}
                return JsonResponse(data=response, safe=False)
    except Recipe.DoesNotExist:
        response = {'retcode': 1, 'msg': '数据查询失败'}
        return JsonResponse(response)


@require_http_methods("POST")
def notify(request):
    """微信支付回调"""
    Pay = WeChatPay(appid=settings.WECHAT_PAY['APPID'], mch_id=settings.WECHAT_PAY['MCHID'],
                    api_key=settings.WECHAT_PAY['APIKEY'], sandbox=settings.WECHAT_PAY['SANDBOX'])
    try:
        result = Pay.parse_payment_result(request.body)
    except Exception as e:
        print(str(e))
        return HttpResponse("FAIL")
    if result['result_code'] == "SUCCESS" and result['return_code'] == "SUCCESS":
        out_trade_no = result['out_trade_no']
        queryResult = Pay.order.query(out_trade_no=out_trade_no)
        if queryResult['trade_state'] == "SUCCESS":  # 主动查询支付状态
            # 查询数据库，修改数据库，通知his支付完成
            querySet = Payment.objects.filter(orderNo=out_trade_no, status=1)
            if querySet.exists():
                time_end = result['time_end']
                time_str = "%s年%s月%s日 %s时%s分%s秒" % (time_end[0:4], time_end[4:6], time_end[6:8], time_end[8:10],
                                                    time_end[10:12], time_end[12:14])
                pay_order = querySet[0]
                pay_order.recipe.status = 2
                pay_order.status = 2
                pay_order.transactionID = result['transaction_id']
                pay_order.timeEnd = time_str
                param = {'patientid': pay_order.recipe.patientId, 'cflist': pay_order.recipe.c_list}
                splice_str = param['patientid'] + param['cflist']
                response = post_ask('/api/pay/HisPayApi', param, splice_str)
                if response['Tag'] == 1 or response['Tag'] == '1':
                    pay_order.notify = '1'
                pay_order.save()
                pay_order.recipe.save()
        return HttpResponse("SUCCESS")
    else:
        return HttpResponse("FAIL")


def close_order(no):
    try:
        pay = WeChatPay(appid=settings.WECHAT_PAY['APPID'], mch_id=settings.WECHAT_PAY['MCHID'],
                        api_key=settings.WECHAT_PAY['APIKEY'], sandbox=settings.WECHAT_PAY['SANDBOX'])
        pay.order.close(out_trade_no=no)
        pay_order = Payment.objects.get(orderNo=no)
        pay_order.status = 0
        pay_order.save()
    except Exception as e:
        print(str(e))
        print('失败')


def notify_task(request):
    querySet = Payment.objects.filter(status='2', notify='0')
    for item in querySet:
        param = {'patientid': item.recipe.patientId, 'cflist': item.recipe.c_list}
        splice_str = param['patientid'] + param['cflist']
        response = post_ask('/api/pay/HisPayApi', param, splice_str)
        if response['Tag'] == 1 or response['Tag'] == '1':
            item.notify = '1'
            item.save()
    return JsonResponse({'msg': 'SUCCESS'}, safe=False)
