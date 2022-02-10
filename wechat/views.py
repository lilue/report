import json
import re
from django.shortcuts import render
from wechatpy.utils import check_signature, ObjectDict
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse, JsonResponse
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply, ArticlesReply
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
                elif msg.key == 'image':
                    status = 'image'
                    media_id = '8fXeWJG1lxALWwMtq-yEF5g7v4y__QcDGkCaoBYSPVTRvCIXVgbnNIEHRCuzuO5_'
                    tempMsg = '图片回复'
                else:
                    tempMsg = replayMes()
                news = tempMsg
        elif msg.type == 'text':
            keyword = ['时间', '时候', '上班', '几时']
            for i in keyword:
                result = i in msg.content
                if result:
                    break
            if result:
                news = '急诊科及120急救、住院病房均24小时工作制，门诊、医保报销、预防保健科工作日正常上班，' \
                          '8:00—11:30、14:30—17:30，周六8:00—11:30，如特殊情况，可联系医院或相关医护人员。'
            else:
                item_str = msg
                if '*' in msg.content:
                    res = getInfo(item_str)
                else:
                    res = replayMes()
                news = res
        else:
            news = replayMes()
        if status == 'text':
            reply = TextReply(content=news, message=msg)
        elif status == 'image':
            reply = ImageReply(media_id=media_id, message=msg)
            # print(reply)
        elif status == 'article':
            reply = ArticlesReply(message=msg)
            reply.add_article(article)
        response = HttpResponse(reply.render(), content_type='application/xml')
        return response


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
    res = '非常感谢您的留言，如在上班时间我们将第一时间回复，如节假日因48小时未回复，按微信平台规则不能再回复，敬请谅解！\n' \
          '预约核酸检测请拨打院务办电话3821203，每天上午8:00-11:30及下午14:30-17:00为核酸采样时间，具体以医务科的安排为准，' \
          '检验报告方面上午采样的，当天晚上可以查询结果，下午采样的第二天晚上可以查询结果；\n' \
          '如预约四维彩超，由于咨询预约人数较多，请到妇产科具体咨询；\n' \
          '如预约疫苗接种，请在微信公众号页面右下角便民服务中的预约服务按要求填写小孩资料预约，新生儿疫苗接种预约同上，谢谢！\n' \
          '如需查询并下载新冠核酸检验结果，请发送【采样时登记的手机号码或电话号码*证件号】获取。例：13123456789*441234567894561235'
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
def getMaterialsList(request, offset):
    client = WeChatClient(settings.APP_ID, settings.APP_SECRET)
    materials_list = client.material.batchget(media_type='image', offset=offset, count=350)
    # materials_list = client.material.batchget(media_type='news')
    return JsonResponse(materials_list, json_dumps_params={'ensure_ascii': False})


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
                            "type": "view",
                            "name": "医院简介",
                            "url": "http://mp.weixin.qq.com/s?__biz=MzI1MjU0MTMzOQ==&mid=100000003&idx=1&sn"
                                   "=d5cf1a1121d979086dad9f2e01d52ed1&chksm"
                                   "=69e361f75e94e8e1c1c6c51ec9fc633c4cb706cd92e92954eca948ff631ab088d2aad9762f42"
                                   "&scene=18#wechat_redirect "
                        },
                        {
                            "type": "view",
                            "name": "楼层布局",
                            "url": "http://mp.weixin.qq.com/s?__biz=MzI1MjU0MTMzOQ==&mid=100000018&idx=1&sn"
                                   "=ff39a0c7e966e5093d9965243b2d7c0c&chksm"
                                   "=69e361e65e94e8f0cfd24923a7ba8b2b26da91e03cf2c11642b5d4f7de5a66f1c893c60a5276"
                                   "&scene=18#wechat_redirect "
                        },
                        {
                            "type": "click",
                            "name": "来院线路",
                            "key": "route"
                        },
                        {
                            "type": "view",
                            "name": "招聘信息",
                            "key": "http://mp.weixin.qq.com/s?__biz=MzI1MjU0MTMzOQ==&mid=2247484762&idx=1&sn"
                                   "=ef96ea38bc448bded2a11f3d65e7f839&chksm"
                                   "=e9e365aede94ecb8fefd8c56f98712bcca0c04197a08f34a44f3c045279791c78285f548856c"
                                   "&scene=18#wechat_redirect "
                        },
                    ]
                },
                {
                    "name": "就诊服务",
                    "sub_button": [
                        {
                            "type": "click",
                            "name": "健康申报卡",
                            "key": "health"
                        },
                        {
                            "type": "img",
                            "name": "电子陪护证",
                            "value": "VGSuBmSVPkhR8yhfeYakY01_EtEOhzcm8MKPKqWUpVkCQkptcQhLMD3zK08KuNYj"
                        },
                        {
                            "type": "view",
                            "name": "通知公告",
                            "url": "http://mp.weixin.qq.com/mp/homepage?__biz=MzU4ODA1NTAyNg==&hid=2&sn=29b38ba124689f3220bee403e7afb0aa&scene=18#wechat_redirect"
                        },
                        {
                            "type": "view",
                            "name": "公共卫生宣传",
                            "url": "http://mp.weixin.qq.com/mp/homepage?__biz=MzU4ODA1NTAyNg==&hid=3&sn=e3190f3cf3a56e39a2f169881e61e58f&scene=18#wechat_redirect"
                        },
                        {
                            "type": "view",
                            "name": "孕前检查",
                            "url": "http://mp.weixin.qq.com/s?__biz=MzU4ODA1NTAyNg==&mid=100000986&idx=1&sn=fd63f6fcd1adf8e08d5f77d7f0c5a3cd&chksm=7de3ec474a9465517978e656d9061fd72d119e2929388e98bcb2a2fe23a0d38726b80d5a1cb6&scene=18#wechat_redirect"
                        },
                    ]
                },
                {
                    "name": "便民服务",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "停车缴费",
                            "url": "http://wx.ymiot.net/dwz?p=c1gd9dsk"
                        },
                        {
                            "type": "view_limited",
                            "name": "疫苗种类接种时间",
                            "media_id": "HmciRG5xP_jEQD0HuE5bFHt0ItcB8Vxhwkk1-VHpuSA"
                        },
                        {
                            'type': 'miniprogram',
                            'name': '预约疫苗接种',
                            'url': 'https://app.cn2030.com/html/xiaochengxu.html',
                            'appid': 'wx2c7f0f3c30d99445',
                            'pagepath': 'tabs/tab_1/tab_1'
                        },
                        {
                            'type': 'view',
                            'name': '满意度调查',
                            'url': 'https://www.wjx.cn/jq/13633050.aspx'
                        },
                    ]
                }
            ]
        }
        # print(menuList)
        # print(type(menuList))
        # client.menu.create(menuList)
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
