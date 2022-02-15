import json
import re
from utils.json_data import jsonData
import requests
from django.shortcuts import render
from wechatpy.utils import check_signature, ObjectDict
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse, JsonResponse
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply, ArticlesReply, EmptyReply
from reports.models import Report, Subscription
# from wage.models import Payroll
from wechatpy import WeChatClient
from report import settings
from django.views.decorators.csrf import csrf_exempt
from utils.process import process_date


# Create your views here.


@csrf_exempt
def handle_wx(request):
    # GET 方式用于微信公众
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(settings.TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = '错误的请求'
        response = HttpResponse(echo_str)
        return response
    else:
        # print(request.body)
        msg = parse_message(request.body)
        status = 'text'
        if msg.type == 'event':
            if msg.event == 'subscribe':
                news = '欢迎关注"湛江市赤坎区人民医院"\n我们将竭诚为您服务，为您的健康保驾护航！\n地址：湛江市赤坎区民主路73号'
            elif msg.event == 'click':
                article = ObjectDict()
                if msg.key == 'vaccine':
                    status = 'article'
                    tempMsg = '疫苗'
                elif msg.key == 'route':
                    tempMsg = "①【11路，12路，13路，15路，16路，1路，22路，23路，25路，27路，29路，2路，33路，809路，8路】-南华广场站，往民主路方向步行680米。\n②【21" \
                              "路，29路东线，809路，821路】-民主路中站，往幸福路方向步行50米。 "
                else:
                    tempMsg = replayMes()
                news = tempMsg
        elif msg.type == 'text':
            item_str = msg
            if '*' in msg.content:
                res = getInfo(item_str)
            else:
                res = replayMes()
                client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
                datalist = getJson(msg.content)
                for item in datalist:
                    if item['type'] == 'text':
                        client.message.send_text(msg.source, item['content'])
                        status = 'send'
                        # reply = TextReply(content=item['content'], message=msg)
                    elif item['type'] == 'img':
                        client.message.send_image(msg.source, item['content'])
                        status = 'send'
                    elif item['type'] == 'news':
                        try:
                            news_info = item['news_info']['list'][0]
                            article = {
                                "title": news_info['title'],
                                "description": news_info['digest'],
                                "url": news_info['content_url'],
                                "thumb_url": news_info['cover_url']
                            }
                            client.message.send_link(msg.source, article)
                        except Exception as e:
                            print(str(e))
                        status = 'send'
                # return HttpResponse(reply.render(), content_type='application/xml')
            news = res
        else:
            news = replayMes()
        if status == 'text':
            reply = TextReply(content=news, message=msg)
            # print(reply)
        elif status == 'article':
            reply = ArticlesReply(message=msg)
            reply.add_article(article)
        elif status == 'send':
            reply = EmptyReply()
        return HttpResponse(reply.render(), content_type='application/xml')


def getInfo(params):
    # print(params.content)
    symbol = '*'
    msg = params.content
    # open_id = params.source
    # print(open_id)
    response = symbol in msg
    if response:
        text = msg.split(symbol, 1)
        query_set = Report.objects.filter(phone=text[0], idCard=text[1]).order_by('-id')[:1]
        if query_set.exists():
            # 有数据
            template = "【新型冠状病毒(COVID-19)核酸检测结果】\n" \
                       "姓名：%s\n" \
                       "采样机构：%s\n" \
                       "检测机构：湛江市赤坎区人民医院\n" \
                       "检测日期：%s\n" \
                       "检测结果：%s\n" \
                       "此报告仅对所检验标本负责，如有疑议请在三天内与检验科联系！\n" \
                       "PDF版报告：【%s】, 请复制至浏览器打开。"
            for report in query_set:
                if not report.zjg:
                    zjg = '阴性(-)'
                else:
                    zjg = report.zjg
                str_ss = report.inspection_date.split(' ', 1)
                folder = process_date(report.inspection_date)
                pdfUrl = "https://image.zhonghefull.com/ckpdf/%s/%s.pdf" % (folder, report.idCard)
                result = template % (report.name, report.hospital, str_ss[0], zjg, pdfUrl)
        else:
            result = "暂无证件号%s的检验结果，请稍后查询。" % (text[1])
    else:
        result = replayMes()
    return result


# 工资查询，赤坎没有该功能
# def getSlip(params):
#     # code = params.replace('gz', '')
#     # query_set = Payroll.objects.filter(random_code=code).order_by('-id')[:1]
#     text = params.split('+', 1)
#     query_set = Payroll.objects.filter(idCard=text[0], random_code=text[1]).order_by('-id')[:1]
#     if query_set.exists():
#         for i in query_set:
#             res = i.content
#     else:
#         res = replayMes()
#     return res


def replayMes():
    res = '您的留言我们已收到，我们将会尽快回复，感谢您的关注！\n' \
          '如需查询并下载新冠核酸检验结果，请发送【采样时登记的手机号码或电话号码*证件号】获取。例：13123456789*441234567894561235'
    # '如需查询并下载新冠核酸检验结果，请发送【采样时登记的手机号码或电话号码*证件号】获取。例：13123456789*441234567894561235'
    return res


def menu(request):
    return render(request, 'wechat/menu.html')


@csrf_exempt
def getMenu(request):
    client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
    # client = WeChatClient("wx896da0e215f91253", "21df20f1f63944f9f0eeb65e5a5e6450")
    menu_info = client.menu.get()
    # print(menu_info)
    # print(menu_info['selfmenu_info'])
    return JsonResponse(menu_info, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def getMaterialsCount(request):
    client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
    materials_count = client.material.get_count()
    return JsonResponse(materials_count, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def getMaterialsList(request, media, offset):
    client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
    # media 分别有图片（image）、语音（voice）、视频（video）和缩略图（news）
    materials_list = client.material.batchget(media_type=media, offset=offset, count=350)
    # materials_list = client.material.batchget(media_type='news')
    return JsonResponse(materials_list, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def getBatchget(request, offset):
    client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
    access_token = client.fetch_access_token()
    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token=' + access_token['access_token']
    data = {
        "offset": offset,
        "count": 20,
        "no_content": 0
    }
    response = requests.post(url=API_BASE_URL, json=data)
    result = json.loads(response.text)
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def getMessageList(request):
    client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
    messageList = client.message.get_autoreply_info()
    return JsonResponse(messageList, json_dumps_params={'ensure_ascii': False})


def createMenu(request):
    if request.method == 'GET':
        client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
        # client = WeChatClient("wx34323ffaf43c7824", "4c50c86bc211f62145076d93c8d089f8")  # 坡头
        # client = WeChatClient("wx896da0e215f91253", "21df20f1f63944f9f0eeb65e5a5e6450")
        menuList = {
            "button": [
                {
                    "name": "医院概况",
                    "sub_button": [
                        {
                            "type": "view_limited",
                            "name": "医院简介",
                            "media_id": "VGSuBmSVPkhR8yhfeYakYwpevUxs16MCwqpImOOuhY9Hb6Rg5kTb5bLuCvFfIA_j"
                        },
                        {
                            "type": "view_limited",
                            "name": "楼层布局",
                            "media_id": "VGSuBmSVPkhR8yhfeYakY8vleeiGR9lnPRnAwuaI55H1b72evkVbGeZmTDpSU4Ji"
                        },
                        {
                            "type": "click",
                            "name": "来院线路",
                            "key": "route"
                        },
                        {
                            "type": "view_limited",
                            "name": "招聘信息",
                            "media_id": "VGSuBmSVPkhR8yhfeYakY0BjbKqWdddFZKcnbQU9Y0SK5PesCez-5r1ptxvpU3GW"
                        },
                    ]
                },
                {
                    "name": "就诊服务",
                    "sub_button": [
                        {
                            "type": "media_id",
                            "name": "健康申报卡",
                            "media_id": "VGSuBmSVPkhR8yhfeYakY-DxZlC9KD8r2KXtVp0AxXp3ANj3taScfsG_uJJzByFd"
                        },
                        {
                            "type": "media_id",
                            "name": "电子陪护证",
                            "media_id": "VGSuBmSVPkhR8yhfeYakY01_EtEOhzcm8MKPKqWUpVkCQkptcQhLMD3zK08KuNYj"
                        },
                        {
                            "type": "media_id",
                            "name": "就医须知",
                            "media_id": "VGSuBmSVPkhR8yhfeYakYypnwiiJyUZYNsHcy9VdwQOzXyCoqDyNaArC1eL2qNDH"
                        },
                        {
                            "type": "view",
                            "name": "预约挂号",
                            "url": "https://app.hospital-payment.com/zjsckqrmyy/register?appid=wxc9bc2330d8cd6664"
                        },
                        {
                            "type": "view",
                            "name": "满意度调查",
                            "url": "https://www.wjx.cn/vm/OJaf8nU.aspx"
                        },
                    ]
                },
                {
                    "name": "便民服务",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "健康证驾驶证体检",
                            "url": "http://mp.weixin.qq.com/s?__biz=MzI1MjU0MTMzOQ==&mid=2247484748&idx=1&sn"
                                   "=93446a175ddc35111bfcba283529e612&chksm"
                                   "=e9e365b8de94ecae180eba472cc07d30e3e24d32e2425b1652ecca37353e0b0b210087ddf21b"
                                   "&scene=18#wechat_redirect "
                        },
                        {
                            "type": "view_limited",
                            "name": "核酸检测",
                            "media_id": "VGSuBmSVPkhR8yhfeYakYy107VXMZAoWaYMejvxsG6053nQ9Pbg8oT8Em8284qQ3"
                        },
                        {
                            "type": "media_id",
                            'name': '犬伤疫苗接种',
                            "media_id": "VGSuBmSVPkhR8yhfeYakYwmlPcpr94JG6p2tf_MVcsXt6G5aglpWxQ0Cmmki7fqx"
                        },
                        {
                            'type': 'view_limited',
                            'name': '出生证申领',
                            'media_id': 'VGSuBmSVPkhR8yhfeYakY4B435o_9KtoIrYpQLTUVYNmEG4L_DgDZMgxWd0PRE99'
                        },
                    ]
                }
            ]
        }
        # print(menuList)
        # print(type(menuList))
        client.menu.create(menuList)
        return HttpResponse("OK")

    elif request.method == 'POST':
        request_body = request.POST
        request_body.encoding = "utf-8"
        menuList = request_body['menu']
        menuList = json.loads(menuList)
        try:
            client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
            client.menu.create(menuList)
            return JsonResponse({"msg": "修改成功"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "修改出错了，请联系开发人员！" + str(e)}, safe=False)


def getJson(content):
    dd = jsonData()
    res = dd['list']
    # text = '门诊'
    # anchor = False
    for a in res:
        # print(a['keyword_list_info'])
        for b in a['keyword_list_info']:
            if content in b['content']:
                return a['reply_list_info']
    return ''


def uploadImg(request):
    import os
    url = '/Users/lilue/Desktop/title.jpg'
    files = {'file': open(url, 'rb')}
    print(files['file'])
    client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
    aa = client.material.add(media_type='image', media_file=files['file'])
    print(aa)
    return JsonResponse("ddd", safe=False)


def getMaterial(requset, media):
    client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
    res = client.material.get(media)
    return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)
