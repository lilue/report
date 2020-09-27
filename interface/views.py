import base64
import random
import string
from cProfile import label
from typing import Set, Dict, Any, Union, Callable, Tuple

from django.shortcuts import render
from aip import AipOcr
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time
from report import settings
from wechatpy import WeChatClient


# Create your views here.


class CardOcr(View):
    def __init__(self):
        self.APP_ID = '22417331'
        self.API_KEY = 'Q9TmqFPo0A6Gs8MtxwaGvrKY'
        self.SECRET_KET = 'EtoAULXMztFkh1XD20fjLCPt7T4VkiQV'

    def post(self, request):
        imgFile = request.POST.get('img')
        image = imgFile.replace('data:image/png;base64,', '')
        image = base64.b64decode(image)
        idCardSide = "front"
        client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KET)
        result = client.idcard(image, idCardSide)
        print(result)
        response = {'cardInfo': {'name': result['words_result']['姓名']['words'],
                                 'id': result['words_result']['公民身份号码']['words'],
                                 'nation': result['words_result']['民族']['words'],
                                 'address': result['words_result']['住址']['words']},
                    'retcode': 0}
        # response['cardInfo']['name'] = result['words_result']['姓名']['words']
        # response['cardInfo']['id'] = result['words_result']['公民身份号码']['words']
        # response['cardInfo']['nation'] = result['words_result']['民族']['words']
        # response['cardInfo']['address'] = result['words_result']['住址']['words']
        # response['retcode'] = 0
        return JsonResponse(response)


class Obtain(View):
    def post(self, request):
        if request.method == 'POST':
            try:
                url = request.POST.get('url')
                wxClient = getWxClient()
                ticket = wxClient.jsapi.get_jsapi_ticket()
                times = int(time.time())
                nonce = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                sign = wxClient.jsapi.get_jsapi_signature(nonce, ticket, times, url)
                data = {'appId': 'wxd5191076ca1f7db7', 'timestamp': times,
                        'nonceStr': nonce, 'signature': sign}
                response = {'data': data, 'retcode': 0}
                return JsonResponse(response)
            except Exception as e:
                print("身份证识别异常")
                print(str(e))


def getWxClient():
    return WeChatClient(settings.APP_ID, settings.APP_SECRET)
