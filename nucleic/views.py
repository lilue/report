import os
import string
import uuid
import time
import random
import hashlib
from urllib.parse import urlsplit
from django.contrib import messages
from django.views import View
from django.urls import reverse
import datetime
from PIL import Image
import qrcode
from django.http import HttpResponse, JsonResponse, Http404, FileResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from wechatpy import WeChatPay, WeChatClient
from wechatpy.oauth import WeChatOAuth
from report import settings
from django.shortcuts import redirect
# Create your views here.
from nucleic.models import QRconfig, Payment
from .utils import formatTime


def getWeChatOAuth(redirect_url):
    sub_status = settings.SUB_STATUS
    if sub_status:
        return WeChatOAuth(settings.WECHAT_PAY['SUB_APPID'], settings.WECHAT_PAY['APPSECRET'], redirect_url,
                           scope="snsapi_userinfo")
    else:
        return WeChatOAuth(settings.WECHAT_PAY['APPID'], settings.WECHAT_PAY['APPSECRET'], redirect_url,
                           scope="snsapi_userinfo")


def getWxClient():
    sub_status = settings.SUB_STATUS
    if sub_status:
        return WeChatClient(settings.WECHAT_PAY['SUB_APPID'], settings.WECHAT_PAY['APPSECRET'])
    else:
        return WeChatClient(settings.WECHAT_PAY['APPID'], settings.WECHAT_PAY['APPSECRET'])


# 定义授权装饰器
def oauth(method):
    def warpper(request, *args, **kwargs):
        if request.session.get('user', None) is None:
            code = request.GET.get('code', None)
            wx_oauth = getWeChatOAuth(request.get_raw_uri())
            url = wx_oauth.authorize_url
            if code:
                wx_oauth.fetch_access_token(code)
                user_info = wx_oauth.get_user_info()
                request.session['user_info'] = user_info
            else:
                return redirect(url)
        return method(request, *args, **kwargs)

    return warpper


@require_http_methods(["GET"])
def home(request):
    queryset = QRconfig.objects.filter(status=True).order_by('-create_time')
    title = settings.SITE_HEADER
    title1 = title[0:title.rfind('核酸')]
    title2 = title[title.rfind('核酸'):]
    return render(request, 'nucleic/home.html', {'queryset': queryset, 'title1': title1, 'title2': title2})


@require_http_methods(["GET"])
def index(request, pk):
    try:
        res = QRconfig.objects.get(pk=pk)
    except QRconfig.DoesNotExist:
        raise Http404("请扫码打开页面。")
    data = {"hospital": res.hospital, "location": res.location, "price": '%0.2f' % res.price,
            "item": res.itemName, "qr_id": str(res.id)}
    return render(request, 'nucleic/infoPage.html', data)


@require_http_methods(['GET'])
def waitingPay(request, pk):
    try:
        pay_order = Payment.objects.get(id=pk, status=1)
        amount = '%.2f' % (pay_order.amount / 100)
        data = {"id": pay_order.id, "appid": settings.WECHAT_PAY['APPID'], "timestamp": pay_order.preTime,
                "nonce_str": pay_order.preNonce, "prepay_id": 'prepay_id=' + pay_order.prepayId,
                "paySign": pay_order.paySign, "amount": amount, "location": pay_order.qr.location,
                "number": pay_order.number}
        # print(data)
    except Payment.DoesNotExist:
        raise Http404("参数错误。请重新下单支付")
    return render(request, 'nucleic/waiting_for_payment.html', data)


@require_http_methods("GET")
def complete(request, pk):
    try:
        paymentCompleted = Payment.objects.get(id=pk)
        # if paymentCompleted.status != 2:
        #     Pay = get_entity()
        #     out_trade_no = paymentCompleted.orderNo
        #     queryResult = Pay.order.query(out_trade_no=out_trade_no)
        #     print(queryResult)
        # if queryResult['result_code'] == "SUCCESS" and queryResult['return_code'] == "SUCCESS" and queryResult[
        #     'trade_state'] == "SUCCESS":  # 主动查询支付状态
        data = {"username": paymentCompleted.patient, "number": paymentCompleted.number,
                "local": paymentCompleted.qr.location,
                "endTime": paymentCompleted.timeEnd, "status": paymentCompleted.status}
        return render(request, 'nucleic/finish.html', data)
    except Payment.DoesNotExist:
        return HttpResponse()


@require_http_methods("GET")
def ticket(request):
    params = request.GET
    out_trade_no = params['out_trade_no']
    order = Payment.objects.get(orderNo=out_trade_no)
    txt = 'https://' + request.get_host() + request.path_info + '?sub_mch_id=%s&out_trade_no=%s&transaction_id=%s' % \
          (params['sub_mch_id'], out_trade_no, order.transactionID)
    my_check_code = hashlib.md5(txt.encode(encoding='UTF-8')).hexdigest()
    result = {'orderNo': order.transactionID, 'itemName': order.qr.itemName, 'amount': '%.2f' % (order.amount / 100),
              'hospital': order.qr.hospital, 'timeEnd': order.timeEnd, 'status': order.status, 'logoUrl': settings.LOGO}
    if my_check_code == params['check_code']:
        result['check'] = True
    else:
        result['check'] = False
    return render(request, 'nucleic/ticket.html', result)


@require_http_methods(["GET"])
def downQr(request, pk):
    if os.path.exists('test.png'):
        os.remove('test.png')
    url_path = 'https://' + request.META['HTTP_HOST'] + '/payment/home/' + pk
    file_name = pk + '.png'
    qr_img = qrcode.make(url_path)
    with open('test.png', "wb") as f:
        qr_img.save(f)
    file = open('test.png', 'rb')
    return FileResponse(file, as_attachment=True, filename=file_name)


@require_http_methods(["POST"])
def payment(request):
    people = request.POST.get('people')
    name = request.POST.get('name')
    # total = request.POST.get('total')
    price = request.POST.get('price')
    verificationAmount = int(int(people) * (float(price) * 100))
    # print(verificationAmount)
    user_info = request.session.get('user_info')
    # pr_id = request.POST.get('pr_id')
    qr_id = request.POST.get('qr_id')
    idcard = request.POST.get('idcard')
    phone = request.POST.get('phone')
    present = datetime.datetime.now()
    before = present + datetime.timedelta(hours=-1, minutes=30)
    try:
        order = Payment.objects.get(openid=user_info['openid'], amount=verificationAmount, status=1,
                                    create_time__range=(before, present))
        orderNo = order.id
    except Payment.DoesNotExist:
        orderNo = unifiedOrder(user_info['openid'], name, verificationAmount, people, idcard, phone, qr_id)
    # 统一下单，把下单结果保存在数据库，把支付表的id返回页面，查询下单结果，并支付。
    return JsonResponse(data={'order': orderNo}, safe=False)


def get_entity():
    sub_status = settings.SUB_STATUS
    # , sub_appid = settings.WECHAT_PAY['SUB_APPID'], sub_mch_id=settings.WECHAT_PAY['SUB_MCHID'],
    if sub_status:
        pay = WeChatPay(appid=settings.WECHAT_PAY['APPID'], sub_appid=settings.WECHAT_PAY['SUB_APPID'],
                        mch_id=settings.WECHAT_PAY['MCHID'], sub_mch_id=settings.WECHAT_PAY['SUB_MCHID'],
                        mch_cert=settings.WECHAT_PAY['MCHCERT'], mch_key=settings.WECHAT_PAY['MCHKEY'],
                        api_key=settings.WECHAT_PAY['APIKEY'], sandbox=settings.WECHAT_PAY['SANDBOX'])
    else:
        pay = WeChatPay(appid=settings.WECHAT_PAY['APPID'], mch_id=settings.WECHAT_PAY['MCHID'],
                        sub_mch_id=settings.WECHAT_PAY['SUB_MCHID'],
                        mch_cert=settings.WECHAT_PAY['MCHCERT'], mch_key=settings.WECHAT_PAY['MCHKEY'],
                        api_key=settings.WECHAT_PAY['APIKEY'], sandbox=settings.WECHAT_PAY['SANDBOX'])
    return pay


def unifiedOrder(openid, username, amount, people, card, phone, q):
    """
    统一下单
    :param phone: 电话号码
    :param card: 证件号码
    :param openid: 下单openid
    :param username: 用户输入的姓名
    :param amount: 缴费金额传入时单位为分
    :param people: 就诊人数
    :param q: qr关联
    :return:
    """
    # print(openid, username, amount, people, p, q)
    order_no = ''.join(str(uuid.uuid1()).split('-'))
    callback = '/payment/callback'
    # print(openid, username, amount, people, order_no)
    description = '就诊人' + username
    pay = get_entity()
    # amount = 1      # 测试用
    res = pay.order.create(trade_type=settings.WECHAT_PAY['TYPE'], body=description, total_fee=amount,
                           notify_url=settings.WECHAT_PAY['NOTIFY'] + callback, user_id=openid, out_trade_no=order_no)
    if res['return_code'] == 'SUCCESS' and res['return_msg'] == 'OK':
        timestamp = int(time.time())
        paySign = pay.jsapi.get_jsapi_signature(prepay_id=res['prepay_id'], timestamp=timestamp,
                                                nonce_str=res['nonce_str'])
        expTime = datetime.datetime.now() + datetime.timedelta(hours=1, minutes=30)
        pay_order = Payment.objects.create(patient=username, number=people, amount=amount, openid=openid, idcard=card,
                                           paySign=paySign, qr_id=q, expDate=expTime, orderNo=order_no, phone=phone,
                                           preNonce=res['nonce_str'], prepayId=res['prepay_id'], preTime=timestamp)
        return pay_order.id
    else:
        return '下单失败'


@require_http_methods("POST")
def notify(request):
    """
    微信支付回调
    :param request:
    :return:
    """
    Pay = get_entity()
    try:
        result = Pay.parse_payment_result(request.body)
    except Exception as e:
        print('微信支付回调错误，' + str(e))
        return HttpResponse("FAIL")
    if result['result_code'] == "SUCCESS" and result['return_code'] == "SUCCESS":
        out_trade_no = result['out_trade_no']
        queryResult = Pay.order.query(out_trade_no=out_trade_no)
        if queryResult['result_code'] == "SUCCESS" and queryResult['return_code'] == "SUCCESS" \
                and queryResult['trade_state'] == "SUCCESS":  # 主动查询支付状态
            # print("主动查询订单状态，支付成功。")
            # 查询数据库，修改数据库
            try:
                pay_order = Payment.objects.get(orderNo=out_trade_no, status=1)
                time_str = formatTime(result['time_end'])
                pay_order.status = '2'
                pay_order.transactionID = result['transaction_id']
                pay_order.timeEnd = time_str
                pay_order.save()
                # tagPrint(pay_order.printer.dsNumber, pay_order.qr.hospital, pay_order.qr.location,
                #          pay_order.patient, pay_order.number, pay_order.transactionID, pay_order.amount,
                #          pay_order.timeEnd, pay_order.qr.itemName)
                # if pay_order.status == '1':
                #     pass
                # else:
                #     print('订单状态不是1，修改过了')
                return HttpResponse("SUCCESS")
            except Payment.DoesNotExist:
                print("回调参数,订单找不到" + result)
                print("可能是已经处理过了，直接返回success")
                try:
                    pa = Payment.objects.get(orderNo=out_trade_no, status=2)
                    return HttpResponse("SUCCESS")
                except Payment.DoesNotExist:
                    return HttpResponse("FAIL")
    else:
        print("主动查询订单状态，支付失败。")
        print("回调参数" + result)
    return HttpResponse("FAIL")


def query(trade_no):
    Pay = get_entity()
    queryResult = Pay.order.query(out_trade_no=trade_no)
    # print(queryResult)
    if queryResult['trade_state'] == 'SUCCESS' and queryResult['trade_state_desc'] == '支付成功':
        return True
    else:
        return False

