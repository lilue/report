from django.shortcuts import render
import reportlab
from django.http import HttpResponse
from wechatpy import WeChatClient
import json
# Create your views here.


def get_menu_info():
    client = WeChatClient('wx34323ffaf43c7824', '4c50c86bc211f62145076d93c8d089f8')
    menu_info = client.menu.get_menu_info()
    print(menu_info)
    response = HttpResponse(json.dumps(menu_info), content_type='application/json')
    return response


def createMenu(request):
    client = WeChatClient("appid", "secret")
    client.menu.add_conditional({
        "button": [
            {
                "name": "医院概括",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "医院介绍",
                        "url": ""
                    },
                    {
                        "type": "view",
                        "name": "康复医学",
                        "url": ""
                    },
                    {
                        "type": "click",
                        "name": "医院分布",
                        "url": ""
                    },
                    {
                        "type": "click",
                        "name": "来院线路",
                        "url": ""
                    },
                    {
                        "type": "click",
                        "name": "联系我们",
                        "url": ""
                    },
                ]
            }
        ]
    })
    pass
