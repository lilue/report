import json
import utils.response
from django.core import serializers
from django.http import JsonResponse
from django.views import View
from reports.models import Report
from utils.response import wrap_json_response, ReturnCode, CommonResponseMixin
from utils.auth import already_authorized, c2s
from .models import User
from invoice.models import Invoice

# Create your views here.


def test_session(request):
    phone = '14767922931'
    idcard = '440804200709251657'
    query_set = Report.objects.filter(phone=phone, idCard=idcard).order_by('-id')[:1]
    for report in query_set:
        print(report.zjg)
    request.session['message'] = 'Test Django Session OK!'
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


def logout(request):
    request.session.clear()
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)
    pass


class UserView(View, CommonResponseMixin):
    """
    获取发票列表
    """
    def get(self, request):
        openid = request.GET["openid"]
        try:
            user = User.objects.get(open_id=openid)
            query_set = user.invoice_set.all().order_by("-id")
            invoice_list = []
            if query_set.exists():
                for i in query_set:
                    invoice_list.append(i.to_dict())
            # print(invoice_list)
            # response = {'message': '保存成功'}
            response = utils.response.wrap_json_response(data=invoice_list)
            return JsonResponse(data=response, safe=False)
        except Exception as e:
            # print(str(e))
            response = self.wrap_json_response(data=str(e), code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)

    """
    保存发票
    """
    def post(self, request):
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        data_source = post_data.get('data')
        print(data_source)
        try:
            user = User.objects.get(open_id=data_source['openid'])
            # print(user.nickname)
            invoice = Invoice.objects.filter(number=data_source['number'])
            if invoice:
                response = self.wrap_json_response(data='发票代码与发票号码重复，请检查', code=ReturnCode.FAILED)
                # response = {'message': '发票代码与发票号码重复，请检查'}
            else:
                Invoice.objects.create(number=data_source['number'], code=data_source['code'],
                                       seller=data_source['seller'], seller_number=data_source['seller_number'],
                                       amount=data_source['amount'], purchaser=data_source['purchaser'],
                                       purchaser_number=data_source['purchaser_number'], date=data_source['date'],
                                       confirm=False, user=user)
                # response = {'message': '保存成功'}
                response = self.wrap_json_response(code=ReturnCode.SUCCESS)
        except Exception as e:
            # response = {'message': '用户信息错误，请重新登录后再保存'}
            response = self.wrap_json_response(data='用户信息错误，请重新登录后再保存', code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)

        # print(dd)
        # response = {'message': 'post.'}
        return JsonResponse(data=response, safe=False)

    """
    删除接口
    """
    def delete(self, request):
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        pk = post_data.get('pk')
        try:
            i = Invoice.objects.get(pk=pk)
            i.delete()
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
        except Exception as e:
            print(str(e))
            response = self.wrap_json_response(code=ReturnCode.FAILED)
        return JsonResponse(data=response, safe=False)



def __authorize_by_code(request):
    """
    使用wx.login得到的临时code到微信提供的code2session接口授权
    """
    response = {}
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    code = post_data.get('code').strip()
    avatar = post_data.get('avatar').strip()
    nickname = post_data.get('nickname').strip()
    if not code:
        response['message'] = '数据不完整.'
        response['code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        return JsonResponse(data=response, safe=False)
    data = c2s(code)
    openid = data.get('openid')
    print('get openid:', openid)
    if not openid:
        response = wrap_json_response(code=ReturnCode.FAILED, message='auth failed')
        return JsonResponse(data=response, safe=False)
    request.session['open_id'] = openid
    request.session['is_authorized'] = True

    if not User.objects.filter(open_id=openid):
        new_user = User(open_id=openid, nickname=nickname, avatar=avatar)
        print('new user: open_id: %s,nickname: %s' % (openid, nickname))
        new_user.save()
    user = User.objects.filter(open_id=openid)
    for i in user:
        if i.avatar != avatar:
            i.avatar = avatar
            i.save()
    json_data = serializers.serialize('json', user)
    response = wrap_json_response(code=ReturnCode.SUCCESS, message=json_data)
    response['data'] = 'this is data.'
    return JsonResponse(data=response, safe=False)


def authorize(request):
    return __authorize_by_code(request)

