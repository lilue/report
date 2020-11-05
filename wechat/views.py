import json
import re
from django.shortcuts import render
from wechatpy.utils import check_signature, ObjectDict
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply, ArticlesReply
from reports.models import Report, Subscription
from wage.models import Payroll
from wechatpy import WeChatClient
from django.views.decorators.csrf import csrf_exempt
from utils.process import process_date

#  token 取自微信公众号自己设置的
token = 'JVWsgSgWG5Lu2z4jEE7OGRY18ixvJm4'


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
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = '错误的请求'
        response = HttpResponse(echo_str)
        return response
    else:
        msg = parse_message(request.body)
        status = 'text'
        if msg.type == 'event':
            if msg.event == 'subscribe':
                news = '非常感谢您关注湛江市坡头区人民医院，预约核酸检测请拨打医务科电话3822802，' \
                          '每天早上8点至10点为核酸采样时间，具体以医务科的安排为准，检验报告请咨询检验科3822806；' \
                          '如预约四维彩超，由于咨询预约人数较多，请到妇产科具体咨询；如预约疫苗接种，' \
                          '请在微信公众号页面右下角便民服务中的预约服务按要求填写小孩资料预约，新生儿疫苗接种预约同上，谢谢！'
            elif msg.event == 'click':
                article = ObjectDict()
                if msg.key == 'vaccine':
                    status = 'article'
                    tempMsg = '疫苗'
                elif msg.key == 'family':
                    status = 'article'
                    tempMsg = '家庭医生'
                elif msg.key == 'hospital':
                    status = 'article'
                    article.title = '坡头镇家庭医生服务团队名单及服务所属自然村'
                    article.description = ''
                    article.image = 'http://mmbiz.qpic.cn/mmbiz_jpg/CYRHfvAwum0Aib4ZXsPDgibHIiauJw1SPH1tWAE7cvBmt33WhjCgBqsFeQT2EwaeDobN6qVpqB4ibzT6z6iauR1Ombg/0?wx_fmt=jpeg'
                    article.url = 'http://mp.weixin.qq.com/s?__biz=MzU4ODA1NTAyNg==&mid=100000221&idx=1&sn=7421bd9c8ee87945e60328170030e128&chksm=7de3e9404a946056bd11a5587d8e32416bccb306b4bc4e1b4c2dc17efd665cc7b36a769c4ef6#rd'
                    tempMsg = '医院分布'
                elif msg.key == 'text':
                    tempMsg = '院务办公：0759-3821203\n急救电话：0759-3823120\n防疫电话：0759-3821379\n' \
                              '妇产科电话：0759-3822013\n邮箱：2653809347@qq.com\n地址：湛江市坡头区坡头镇红旗路18-20号'
                elif msg.key == 'image':
                    status = 'image'
                    media_id = '8fXeWJG1lxALWwMtq-yEF5g7v4y__QcDGkCaoBYSPVTRvCIXVgbnNIEHRCuzuO5_'
                    tempMsg = '图片回复'
                else:
                    tempMsg = '非常感谢您关注湛江市坡头区人民医院，预约核酸检测请拨打医务科电话3822802，' \
                          '每天早上8点至10点为核酸采样时间，具体以医务科的安排为准，检验报告请咨询检验科3822806；' \
                          '如预约四维彩超，由于咨询预约人数较多，请到妇产科具体咨询；如预约疫苗接种，' \
                          '请在微信公众号页面右下角便民服务中的预约服务按要求填写小孩资料预约，新生儿疫苗接种预约同上，谢谢！'
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
                if '+' in msg.content:
                    res = getSlip(msg.content)
                elif '*' in msg.content:
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
            print(reply)
        elif status == 'article':
            reply = ArticlesReply(message=msg)
            reply.add_article(article)
        response = HttpResponse(reply.render(), content_type='application/xml')
        return response


@csrf_exempt
def render(request):
    if request.method == 'GET':
        client = WeChatClient('wxd5191076ca1f7db7', '5a20659127d67fe81a9ea9a84dd3da8a')
        res = client.message.send_text('ozCtJt2NDcPEJ3lJCC9CezBFmH2g', '测试主动发消息')
        response = HttpResponse(json.dumps(res), content_type='application/json')
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
                       "检测日期：%s\n" \
                       "检测机构：湛江市坡头区人民医院\n" \
                       "检测结果：%s\n" \
                       "此报告仅对所检验标本负责，如有疑议请在三天内与检验科联系！\n" \
                       "PDF版报告：【%s】, 请复制至浏览器打开。"
            for report in query_set:
                # temporary = report.report_date.split(' ', 1)
                # print(type(report.report_date))
                # print(report.report_date)
                folder = process_date(report.inspection_date)
                pdfUrl = "https://image.zhonghefull.com/pdf/%s/%s_%s.pdf" % (folder, folder, report.sample_num)
                result = template % (report.name, report.inspection_date, report.proposal,  pdfUrl)
        else:
            result = "暂无证件号%s的检验结果，请稍后查询。" % (text[1])
    else:
        result = replayMes()
    return result


def getSlip(params):
    # code = params.replace('gz', '')
    # query_set = Payroll.objects.filter(random_code=code).order_by('-id')[:1]
    text = params.split('+', 1)
    query_set = Payroll.objects.filter(idCard=text[0], random_code=text[1]).order_by('-id')[:1]
    if query_set.exists():
        for i in query_set:
            res = i.content
    else:
        res = replayMes()
    return res


def replayMes():
    res = '非常感谢您的留言，如在上班时间我们将第一时间回复，如节假日因48小时未回复，按微信平台规则不能再回复，敬请谅解！\n' \
          '预约核酸检测请拨打医务科电话3822802，每天8点至11点及14:30至16:30为核酸采样时间。\n' \
          '如预约四维彩超，由于咨询预约人数较多，请到妇产科具体咨询；\n' \
          '如预约疫苗接种，请在微信公众号页面右下角便民服务中的预约服务按要求填写小孩资料预约，新生儿疫苗接种预约同上，谢谢！\n' \
          '如需查询并下载新冠核酸检验结果，请发送【采样时登记的手机号码或电话号码*证件号】获取。\n' \
          '例：13123456789*441234567894561235查询\n' \
          '报告时间：上午采样的，当天晚上可以查询结果，下午采样的第二天晚上可以查询结果。'
    return res


def createMenu(request):
    if request.method == 'GET':
        client = WeChatClient("wx34323ffaf43c7824", "4c50c86bc211f62145076d93c8d089f8")  # 坡头
        # client = WeChatClient("wxd5191076ca1f7db7", "5a20659127d67fe81a9ea9a84dd3da8a")
        client.menu.create({
            "button": [
                {
                    "name": "医院概括",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "医院介绍",
                            "url": "https://mp.weixin.qq.com/s/djuFaVy6RFYmaA49tFGQoA"
                        },
                        {
                            "type": "view",
                            "name": "康复医学",
                            "url": "https://v.youku.com/v_show/id_XNDQ5MjE0OTg1Mg=="
                        },
                        {
                            "type": "view_limited",
                            "name": "医院分布",
                            "media_id": "HmciRG5xP_jEQD0HuE5bFN2L8AxiMgyNnIxkwYV9c_w"
                        },
                        {
                            "type": "click",
                            "name": "来院路线",
                            "key": "image"
                        },
                        {
                            "type": "click",
                            "name": "联系我们",
                            "key": "text"
                        },
                    ]
                },
                {
                    "name": "医院资讯",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "医院动态",
                            "url": "http://mp.weixin.qq.com/mp/homepage?__biz=MzU4ODA1NTAyNg==&hid=1&sn=47bb912d49328559ae48fdc8369ecf4d&scene=18#wechat_redirect"
                        },
                        {
                            "type": "view_limited",
                            "name": "家庭医生服务团队",
                            "media_id": "HmciRG5xP_jEQD0HuE5bFPl2PYR2iAGPxN2Sd4HdW2E"
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
                            "type": "view",
                            "name": "核酸检测",
                            "url": "https://www.wjx.cn/jq/81216464.aspx"
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
        })
        return HttpResponse("OK")
