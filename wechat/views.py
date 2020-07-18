import json
import re
from wechatpy.replies import TextReply
from django.shortcuts import render
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse
from wechatpy import parse_message
from wechatpy.replies import TextReply
from reports.models import Report, Subscription
from wechatpy import WeChatClient

#  token 取自微信公众号自己设置的
token = 'test'


# Create your views here.

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
        if msg.type == 'text':
            item_str = msg
            res = getInfo(item_str)
            content = res
        else:
            content = '请发送电话号+证件号查询检验结果。例：13123456789*441234567894561235'
        reply = TextReply(content=content, message=msg)
        response = HttpResponse(reply.render(), content_type='application/xml')
        return response


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
            template = "姓名：%s\n性别：%s\n年龄：%s\n采样时间：%s\n样本状态：%s\n送检医院：%s\n" \
                       "联系方式：%s\n证件号：%s\n" \
                       "检验结果：%s\n检验日期：%s\n报告日期：%s\n检验者：%s\n审核者：%s\n" \
                       "此报告仅对所检验标本负责，如有疑议请在三天内与检验科联系！"
            for report in query_set:
                print(report)
                result = template % (report.name, report.gender, report.age, report.sampling_time, report.sample_status,
                                     report.hospital, report.phone, report.idCard, report.proposal,
                                     report.inspection_date, report.report_date, report.examiner, report.reviewer)
        else:
            phone_res = re.match("^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$", text[0])
            id_card_res = re.match("/^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(("
                      "[0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$", text[1])
            if not phone_res or not id_card_res:
                result = "输入格式不正确，请检查后重新发送。"
            if phone_res and id_card_res:
                result = "暂无手机号%s，证件号%s的检验结果，请稍后查询。" % (text[0], text[1])
    else:
        result = '请发送电话号+证件号查询检验结果。例：13123456789*441234567894561235'
    return result
