from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from wechatpy import WeChatClient
from wechatpy.replies import BaseReply
from wechatpy.oauth import WeChatOAuth
from report import settings
from .models import UserProfile, UserCard
from django.shortcuts import redirect
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from utils.encrypt import common_api


# Create your views here.


class Management(View):
    def get(self, request):
        user_info = request.session.get('user')
        card_list = []
        if user_info:
            query_set = UserCard.objects.filter(user=user_info['id'])
            for temp in query_set:
                card_list.append(temp.to_dict())
        return render(request, 'health/index.html')

    def post(self, request):
        pass


def getWxClient():
    return WeChatClient(settings.AppID, settings.AppSecret)


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
    def warpper(request):
        if request.session.get('user', None) is None:
            code = request.GET.get('code', None)
            wx_oauth = getWeChatOAuth(request.get_raw_uri())
            url = wx_oauth.authorize_url
            if code:
                try:
                    wx_oauth.fetch_access_token(code)
                    user_info = wx_oauth.get_user_info()
                    # print(user_info['openid'])
                    user = UserProfile.objects.get(openid=user_info['openid'])
                    if user:
                        pass
                    else:
                        user = UserProfile(openid=user_info['openid'], nickname=user_info['nickname'],
                                           head_url=user_info['headimgurl'])
                        user.save()
                    # {'openid': 'ozCtJt2NDcPEJ3lJCC9CezBFmH2g', 'nickname': 'ʟɪʟᴜᴇ_', 'sex': 1, 'language': 'zh_CN',
                    #  'city': '', 'province': '', 'country': '中国',
                    #  'headimgurl': 'http://thirdwx.qlogo.cn/mmopen/vi_32/gcqD8XSIafZADX0lzjsSjEb4kQR14o1EWk7ILBvrXvYY83rGvgBeK60717V6J5mJViaKdjhUFmoVY7xzicMDdg/132',
                    #  'privilege': ['chinaunicom']}
                except Exception as e:
                    print(str(e))
                    # 这里需要处理请求里包含的 code 无效的情况
                    # abort(403)
                else:
                    request.session['user'] = user.to_dict()
                    request.session['user_info'] = user_info
            else:
                return redirect(url)
        return method(request)

    return warpper


@oauth
def get_wx_user_info(request):
    user_info = request.session.get('user')
    return HttpResponse(str(user_info))


@oauth
def add_card(request):
    if request.method == 'GET':
        user = request.session.get('user')
        print(user['openid'])
        # {'id': 1, 'openid': 'ozCtJt2NDcPEJ3lJCC9CezBFmH2g', 'nickname': 'ʟɪʟᴜᴇ_',
        #  'head_url': 'http://thirdwx.qlogo.cn/mmopen/vi_32/gcqD8XSIafZADX0lzjsSjEb4kQR14o1EWk7ILBvrXvYY83rGvgBeK60717V6J5mJViaKdjTAhUFmoVY7xzicMDdg/132'}
        return render(request, 'health/add_card.html')


def post_add_card(request):
    if request.method == 'POST':
        params = request.POST
        session_user = request.session.get('user')
        user = UserProfile.objects.get(openid=session_user['openid'])
        # print(params)
        res = common_api(params['idType'], params['idCard'], 'queryIfHasRegistered')
        if res['datas']['parameters'] == 0:
            print("未注册过")
        else:
            res = common_api(params['idType'], params['idCard'], 'getPersonInfo')
            # print(res['datas'])
            result = res['datas']
            # print(user.usercard_set.all())
            query_set = user.usercard_set.all()
            # print(query_set)
            if query_set.exists():
                for item in query_set:
                    if item.erhc_card_no == res['datas']['erhcCardNo']:
                        print(item.id)      # 卡列表id
            else:
                user_card = UserCard.objects.create(name=params['name'], id_code=params['idCard'],
                                                    erhc_card_no=result['erhcCardNo'], empi=result['empi'],
                                                    user=user)
                print(user_card.id)         # 创建卡id
            # if user.usercard_set:
            #     UserCard.objects.create(name=params['name'], id_code=params['idCard'],
            #                             erhc_card_no=res['datas']['erhcCardNo'], empi=res['datas']['empi'], user=user)
            #     pass
            # else:
            #     pass
            # print("已经注册了")
        return HttpResponse(123)
