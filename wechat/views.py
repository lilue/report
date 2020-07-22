import json
import re
from django.shortcuts import render
from wechatpy.utils import check_signature, ObjectDict
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply, ArticlesReply
from reports.models import Report, Subscription
from wechatpy import WeChatClient

#  token 取自微信公众号自己设置的
token = 'JVWsgSgWG5Lu2z4jEE7OGRY18ixvJm4'


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
        status = 'text'
        if msg.type == 'event':
            if msg.event == 'subscribe':
                content = '非常感谢您关注湛江市坡头区人民医院，预约核酸检测请拨打医务科电话3822802，' \
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
                content = tempMsg
        elif msg.type == 'text':
            keyword = ['时间', '时候', '上班', '几时']
            for i in keyword:
                result = i in msg.content
                if result:
                    break
            if result:
                content = '急诊科及120急救、住院病房均24小时工作制，门诊、医保报销、预防保健科工作日正常上班，' \
                          '8:00—11:30、14:30—17:30，周六8:00—11:30，如特殊情况，可联系医院或相关医护人员。'
            else:
                item_str = msg
                res = getInfo(item_str)
                content = res
        else:
            content = '非常感谢您的留言，如在上班时间我们将第一时间回复，如节假日因48小时未回复，按微信平台规则不能再回复，敬请谅解！\n' \
                      '预约核酸检测请拨打医务科电话3822802，每天早上8点至10点为核酸采样时间，具体以医务科的安排为准，' \
                      '检验报告请咨询检验科3822806；\n如预约四维彩超，由于咨询预约人数较多，请到妇产科具体咨询；\n如预约疫苗接种，' \
                      '请在微信公众号页面右下角便民服务中的预约服务按要求填写小孩资料预约，新生儿疫苗接种预约同上，谢谢！\n' \
                      '如需查询核酸检验结果，请发送【电话号*证件号】查询检验结果。例：13123456789*441234567894561235'
        if status == 'text':
            reply = TextReply(content=content, message=msg)
        elif status == 'image':
            reply = ImageReply(media_id=media_id, message=msg)
        elif status == 'article':
            reply = ArticlesReply(message=msg)
            reply.add_article(article)
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
        phone_res = re.match("^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$", text[0])
        id_card_res = re.match(
            "/^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(("
            "[0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$", text[1])
        if not phone_res or not id_card_res:
            result = "输入格式不正确，请检查后重新发送。"
        else:
            query_set = Report.objects.filter(phone=text[0], idCard=text[1]).order_by('-id')[:1]
            if query_set.exists():
                # 有数据
                template = "新型冠状病毒(COVID-19)核酸检测" \
                           "姓名：%s\n性别：%s\n年龄：%s\n采样时间：%s\n样本状态：%s\n送检医院：%s\n" \
                           "联系方式：%s\n证件号：%s\n" \
                           "检验结果：%s\n检验日期：%s\n报告日期：%s\n检验者：%s\n审核者：%s\n" \
                           "此报告仅对所检验标本负责，如有疑议请在三天内与检验科联系！"
                for report in query_set:
                    result = template % (report.name, report.gender, report.age, report.sampling_time,
                                         report.sample_status, report.hospital, report.phone, report.idCard, report.proposal,
                                         report.inspection_date, report.report_date, report.examiner, report.reviewer)
            else:
                if phone_res and id_card_res:
                    result = "暂无手机号%s，证件号%s的检验结果，请稍后查询。" % (text[0], text[1])
    else:
        result = '非常感谢您的留言，如在上班时间我们将第一时间回复，如节假日因48小时未回复，按微信平台规则不能再回复，敬请谅解！\n' \
                      '预约核酸检测请拨打医务科电话3822802，每天早上8点至10点为核酸采样时间，具体以医务科的安排为准，' \
                      '检验报告请咨询检验科3822806；\n如预约四维彩超，由于咨询预约人数较多，请到妇产科具体咨询；\n如预约疫苗接种，' \
                      '请在微信公众号页面右下角便民服务中的预约服务按要求填写小孩资料预约，新生儿疫苗接种预约同上，谢谢！\n' \
                      '如需查询核酸检验结果，请发送【电话号*证件号】查询检验结果。例：13123456789*441234567894561235'
    return result
