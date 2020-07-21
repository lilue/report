from django.shortcuts import render
import reportlab
from django.http import HttpResponse
from wechatpy import WeChatClient
import json
# Create your views here.


def createMenu(request):
    if request.method == 'GET':
        client = WeChatClient("wx34323ffaf43c7824", "4c50c86bc211f62145076d93c8d089f8")     # 坡头
        # client = WeChatClient("wxd5191076ca1f7db7", "5a20659127d67fe81a9ea9a84dd3da8a")
        client.menu.create({
            "button": [
                {
                    "name": "医院概括",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "医院介绍",
                            "url": "http://mp.weixin.qq.com/s?__biz=MzU4ODA1NTAyNg==&mid=100000735&idx=1&sn=347095cbee115c3b93738c108afbd4d4&chksm=7de3eb424a9462547c62d60ef03572c4fab59f14c4d1d5953f7bd687d0c87d16106db80cab80&scene=18#wechat_redirect"
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
                            "type": "click",
                            "name": "家庭医生服务团队",
                            "key": "family"
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
                            "name": "急救知识",
                            "url": "http://mp.weixin.qq.com/mp/homepage?__biz=MzU4ODA1NTAyNg==&hid=4&sn=d12420be00918fd640bf112d4144b9c4&scene=18#wechat_redirect"
                        },
                        {
                            "type": "click",
                            "name": "疫苗种类接种时间",
                            "key": "vaccine"
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


def getMenu(request):
    if request.method == 'GET':
        client = WeChatClient("wx34323ffaf43c7824", "4c50c86bc211f62145076d93c8d089f8")         # 坡头
        # client = WeChatClient("wxd5191076ca1f7db7", "5a20659127d67fe81a9ea9a84dd3da8a")
        menu_info = client.menu.get_menu_info()
        response = HttpResponse(json.dumps(menu_info), content_type='application/json')
        return response


def get_batchget(request):
    if request.method == 'GET':
        offset = request.GET.get("offset")
        type = request.GET.get("type")
        # client = WeChatClient("wxd5191076ca1f7db7", "5a20659127d67fe81a9ea9a84dd3da8a")
        client = WeChatClient("wx34323ffaf43c7824", "4c50c86bc211f62145076d93c8d089f8")
        count = client.material.batchget(type, offset, 20)
        print(count)
        return HttpResponse("OK")
