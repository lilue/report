from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from wechatpy import WeChatClient
from wechatpy.oauth import WeChatOAuth
from report import settings
from .models import UserProfile, UserCard
from django.shortcuts import redirect
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from utils.interface import card_api, encrypts, get_birth, get_medical
import time


# Create your views here.


class Management(View):
    def get(self, request):
        user_info = request.session.get('user')
        card_list = []
        if user_info:
            query_set = UserCard.objects.filter(user=user_info['id'])
            for temp in query_set:
                card_list.append(temp.to_dict())
        return render(request, 'health/list.html')

    def post(self, request):
        pass


def getWxClient():
    return WeChatClient(settings.APP_ID, settings.APP_SECRET)


def getWxUserInfo(openid):
    wxClient = getWxClient()
    wxUserInfo = wxClient.user.get(openid)
    return wxUserInfo


def getWeChatOAuth(redirect_url):
    return WeChatOAuth(settings.APP_ID, settings.APP_SECRET, redirect_url, scope="snsapi_userinfo")


def wx_verify(request):
    return HttpResponse('PJRLUusp1NXyuD70')


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
                # print(user_info['openid'])
                try:
                    user = UserProfile.objects.get(openid=user_info['openid'])
                    # print(user)
                except UserProfile.DoesNotExist:
                    print('没有用户，抛出异常')
                    user = None
                if user:
                    print("用户已存在，不需要创建")
                else:
                    user = UserProfile(openid=user_info['openid'], nickname=user_info['nickname'],
                                       head_url=user_info['headimgurl'])
                    user.save()
                # {'openid': 'ozCtJt2NDcPEJ3lJCC9CezBFmH2g', 'nickname': 'ʟɪʟᴜᴇ_', 'sex': 1, 'language': 'zh_CN',
                # 'city': '', 'province': '', 'country': '中国', 'headimgurl':
                # 'http://thirdwx.qlogo.cn/mmopen/vi_32
                # /gcqD8XSIafZADX0lzjsSjEb4kQR14o1EWk7ILBvrXvYY83rGvgBeK60717V6J5mJViaKdjhUFmoVY7xzicMDdg/132',
                # 'privilege': ['chinaunicom']} 这里需要处理请求里包含的 code 无效的情况 abort(403)
                request.session['user'] = user.to_dict()
                request.session['user_info'] = user_info
            else:
                return redirect(url)
        return method(request, *args, **kwargs)
    return warpper


@oauth
def get_wx_user_info(request):
    user_info = request.session.get('user')
    return HttpResponse(str(user_info))


class health(View):
    def get(self, request):
        return render(request, 'health/regist_new.html')

    def post(self, request):
        try:
            params = request.POST
            session_user = request.session.get('user')
            user = UserProfile.objects.get(openid=session_user['openid'])
            # print(params)
            p = {'idCode': encrypts(params['idCard']), 'idCardTypeCode': '01'}
            pa = {'name': params['name'], 'idCode': params['idCard'], 'address': params['address'],
                  'birth': get_birth(params['idCard']),
                  'phone': params['phone']}
            res = card_api(p, 'queryIfHasRegistered')
            if '未注册' in res['datas']['remarks']:
                print("未注册过")
                na = '01'
                register_info = {'name': encrypts(params['name']), 'phone': encrypts(params['phone']), 'nation': na,
                                 'personnelType': '1'}
                p.update(register_info)
                register_result = card_api(p, 'createVmcardQRcode')
                if register_result['returnCode'] == 0:
                    print("注册成功")
                    empi = register_result['datas']['empi']
                    erhcCardNo = register_result['datas']['erhcCardNo']
                    qrCode = register_result['datas']['qrCode']
                    try:
                        medical = get_medical(pa)
                    except Exception as e:
                        response = {'retcode': 1, 'msg': str(e)}
                        return JsonResponse(response)
                    user_card = UserCard.objects.create(name=params['name'], id_code=params['idCard'],
                                                        erhc_card_no=erhcCardNo, empi=empi, medical=medical,
                                                        phone=params['phone'], qr_code=qrCode, user=user)
                    user_card.save()
                    card_id = user_card.id
                    card_no = user_card.erhc_card_no
                    print(card_id, card_no)
                    print("新增成功")
            else:
                print("注册过")
                result = card_api(p, 'getPersonInfo')
                result = result['datas']
                # print(result)
                try:
                    query_set = user.usercard_set.filter(erhc_card_no=result['erhcCardNo'])
                    if query_set.exists():
                        print('数据库存在')
                        print(query_set)
                        for item in query_set:
                            card_id = item.id
                            card_no = item.erhc_card_no
                            item.is_untie = 0
                            item.save()
                        print(card_id, card_no)
                    else:
                        tempName = encrypts(result['name'], 'deciphering')
                        tempCode = encrypts(result['idCode'], 'deciphering')
                        tempPhone = encrypts(result['phone'], 'deciphering')
                        receive = card_api(p, 'activateVmcardQRcode')
                        # print(receive['datas']['qrCode'])
                        # print(receive)
                        try:
                            medical = get_medical(pa)
                        except Exception as e:
                            response = {'retcode': 1, 'msg': str(e)}
                            return JsonResponse(response)
                        user_card = UserCard.objects.create(name=tempName, id_code=tempCode,
                                                            erhc_card_no=result['erhcCardNo'], empi=result['empi'],
                                                            phone=tempPhone, qr_code=receive['datas']['qrCode'],
                                                            user=user, medical=medical,)

                        user_card.save()
                        card_id = user_card.id
                        card_no = user_card.erhc_card_no
                        print('数据库不存在，新建一条记录')
                except Exception as e:
                    print(str(e))
                    response = {'retcode': 1, 'msg': str(e)}
                    return JsonResponse(response)
            response = {'retcode': 0, 'id': card_id}
            return JsonResponse(response)
        except Exception as e:
            response = {'retcode': 1, 'msg': str(e)}
            return JsonResponse(response)


def post_add_card(request):
    if request.method == 'POST':
        response = {}
        try:
            params = request.POST
            session_user = request.session.get('user')
            user = UserProfile.objects.get(openid=session_user['openid'])
            # print(params)
            p = {'idCode': params['idCard'], 'idCardTypeCode': params['idType']}
            res = card_api(p, 'queryIfHasRegistered')
            if res['datas']['parameters'] == 0:
                print("未注册过")
            else:
                res = card_api(p, 'getPersonInfo')
                result = res['datas']
                query_set = user.usercard_set.all()
                if query_set.exists():
                    for item in query_set:
                        if item.erhc_card_no == res['datas']['erhcCardNo']:
                            print(item.id)  # 卡列表id
                            card_id = item.id
                            card_no = item.erhc_card_no
                else:
                    user_card = UserCard.objects.create(name=params['name'], id_code=params['idCard'],
                                                        erhc_card_no=result['erhcCardNo'], empi=result['empi'],
                                                        user=user)
                    print(user_card.id)  # 创建卡id
                    card_id = user_card.id
                    card_no = result['erhcCardNo']
            response['msg'] = 'success'
            response['id'] = card_id
            response['cardNo'] = card_no
            response['error_num'] = 0
        except UserProfile.DoesNotExist:
            response['msg'] = '没找到信息'
            response['error_num'] = 1
        return JsonResponse(response)


@require_http_methods(["GET"])
def bind_success(request, no):
    user_card = UserCard.objects.get(id=no)
    data = user_card.to_dict()
    return render(request, 'health/personal.html', data)


@require_http_methods("POST")
def untie_health(request):
    no = request.POST.get('id')
    try:
        user_card = UserCard.objects.get(id=no)
        user_card.is_untie = 1
        user_card.save()
        response = {'retcode': 0, 'msg': '解绑成功'}
    except UserCard.DoesNotExist:
        response = {'retcode': 1, 'msg': '解绑失败，没有找到。'}
    return JsonResponse(response)


@require_http_methods(["GET"])
def health_card_list(request):
    user_info = request.session.get('user')
    user = UserProfile.objects.get(openid=user_info['openid'])
    card_list = user.usercard_set.filter(is_untie=0)
    cards = []
    for item in card_list:
        cards.append(item.to_dict())
    response = {'retcode': 0, 'cards': cards}
    return JsonResponse(response)
