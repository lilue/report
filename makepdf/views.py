from django.shortcuts import render
import reportlab
from django.http import HttpResponse
from wechatpy import WeChatClient
import json
# Create your views here.


def createMenu(request):
    client = WeChatClient("wx34323ffaf43c7824", "4c50c86bc211f62145076d93c8d089f8")
    client.menu.add_conditional({
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
                        "type": "news",
                        "name": "医院分布",
                        'value': 'HmciRG5xP_jEQD0HuE5bFN2L8AxiMgyNnIxkwYV9c_w',
                        'news_info': {
                            {
                                'title': '医院分布',
                                'author': '',
                                'digest': '门诊楼1楼为：急诊科及留观输液室、外科门诊、中西药房、收款',
                                'show_cover': 0,
                                'cover_url': 'http://mmbiz.qpic.cn/mmbiz_jpg/CYRHfvAwum2k12T81VXhxOgzc9VVqB03CsJgZS8xtyxt8uYdttknzTVaDvfg5416SGqHSCAk78u2YQg2xibnGNg/0?wx_fmt=jpeg',
                                'content_url': 'http://mp.weixin.qq.com/s?__biz=MzU4ODA1NTAyNg==&mid=100000177&idx=1&sn=ce76742b0a6338863b2cdce07cde7a3e&chksm=7de3e92c4a94603af8db5a2fa3b65c951c62686d1a98bf26288c7511fdea7f7ccdccaf2c4255#rd',
                                'source_url': ''
                            }
                        }
                    },
                    {
                        "type": "img",
                        "name": "来院线路",
                        'value': '8fXeWJG1lxALWwMtq-yEF5g7v4y__QcDGkCaoBYSPVTRvCIXVgbnNIEHRCuzuO5_'
                    },
                    {
                        "type": "text",
                        "name": "联系我们",
                        'value': '院务办公：0759-3821203\n急救电话：0759-3823120\n防疫电话：0759-3821379\n妇产科电话：0759-3822013\n邮箱：2653809347@qq.com\n地址：湛江市坡头区坡头镇红旗路18-20号'
                    },
                ]
            }, {
                'name': '医院资讯',
                'sub_button': {
                    {
                        'type': 'view',
                        'name': '医院动态',
                        'url': 'http://mp.weixin.qq.com/mp/homepage?__biz=MzU4ODA1NTAyNg==&hid=1&sn=47bb912d49328559ae48fdc8369ecf4d&scene=18#wechat_redirect'
                    }, {
                        'type': 'news',
                        'name': '家庭医生服务团队',
                        'value': 'HmciRG5xP_jEQD0HuE5bFPl2PYR2iAGPxN2Sd4HdW2E',
                        'news_info': {
                            {
                                'title': '坡头镇家庭医生服务团队名单及服务所属自然村',
                                'author': '',
                                'digest': '',
                                'show_cover': 0,
                                'cover_url': 'http://mmbiz.qpic.cn/mmbiz_jpg/CYRHfvAwum0Aib4ZXsPDgibHIiauJw1SPH1tWAE7cvBmt33WhjCgBqsFeQT2EwaeDobN6qVpqB4ibzT6z6iauR1Ombg/0?wx_fmt=jpeg',
                                'content_url': 'http://mp.weixin.qq.com/s?__biz=MzU4ODA1NTAyNg==&mid=100000221&idx=1&sn=7421bd9c8ee87945e60328170030e128&chksm=7de3e9404a946056bd11a5587d8e32416bccb306b4bc4e1b4c2dc17efd665cc7b36a769c4ef6#rd',
                                'source_url': ''
                            }
                        }
                    }, {
                        'type': 'view',
                        'name': '通知公告',
                        'url': 'http://mp.weixin.qq.com/mp/homepage?__biz=MzU4ODA1NTAyNg==&hid=2&sn=29b38ba124689f3220bee403e7afb0aa&scene=18#wechat_redirect'
                    }, {
                        'type': 'view',
                        'name': '公共卫生宣传',
                        'url': 'http://mp.weixin.qq.com/mp/homepage?__biz=MzU4ODA1NTAyNg==&hid=3&sn=e3190f3cf3a56e39a2f169881e61e58f&scene=18#wechat_redirect'
                    }, {
                        'type': 'view',
                        'name': '孕前检查',
                        'url': 'http://mp.weixin.qq.com/s?__biz=MzU4ODA1NTAyNg==&mid=100000986&idx=1&sn=fd63f6fcd1adf8e08d5f77d7f0c5a3cd&chksm=7de3ec474a9465517978e656d9061fd72d119e2929388e98bcb2a2fe23a0d38726b80d5a1cb6&scene=18#wechat_redirect'
                    }
                }
            }, {
                'name': '便民服务',
                'sub_button': {
                    {
                        'type': 'view',
                        'name': '急救知识',
                        'url': 'http://mp.weixin.qq.com/mp/homepage?__biz=MzU4ODA1NTAyNg==&hid=4&sn=d12420be00918fd640bf112d4144b9c4&scene=18#wechat_redirect'
                    }, {
                        'type': 'news',
                        'name': '疫苗种类接种时间',
                        'value': 'HmciRG5xP_jEQD0HuE5bFHt0ItcB8Vxhwkk1-VHpuSA',
                        'news_info': {
                            {
                                'title': '第一类疫苗',
                                'author': '',
                                'digest': '使用规定编辑一、国家免疫规划疫苗常规免疫为：卡介苗接种1剂次；乙肝疫苗接种3剂次；脊灰疫4剂次，前3剂',
                                'show_cover': 0,
                                'cover_url': 'http://mmbiz.qpic.cn/mmbiz_jpg/CYRHfvAwum1uKia7uCQJryQyL8sXgR6aXaMg2drKdFpf0f26Nao5sndr9vvWiboIzYBicJkL27Yl4Pps2zNPsPwJw/0?wx_fmt=jpeg',
                                'content_url': 'http://mp.weixin.qq.com/s?__biz=MzU4ODA1NTAyNg==&mid=100000281&idx=1&sn=dc98a2db8006ac7cbb6edf97325545ae&chksm=7de3ea844a94639202ca3e6e15596a2d63a37b5f92eefcf6b90745b84ab6a1f21e5584ebf3ca#rd',
                                'source_url': ''
                            }, {
                                'title': '第二类疫苗',
                                'author': '',
                                'digest': '第一类疫苗，是指政府免费向公民提供，公民应当依照政府的规定受种的疫苗，包括国家免疫规划确定的疫苗，省、自治',
                                'show_cover': 0,
                                'cover_url': 'http://mmbiz.qpic.cn/mmbiz_jpg/CYRHfvAwum1uKia7uCQJryQyL8sXgR6aXnV83bxymKOtXmfZYw0YdInRz083eM8tY74DZueXUiaC8pkK0lUrCpJg/0?wx_fmt=jpeg',
                                'content_url': 'http://mp.weixin.qq.com/s?__biz=MzU4ODA1NTAyNg==&mid=100000281&idx=2&sn=d4757e375ee74ed9ff8f9d60cab1eeaf&chksm=7de3ea844a946392cc2d6db076d8e8506d2bc049157172fbc43e74cb6745737dc8b0cc806c66#rd',
                                'source_url': ''
                            }
                        }
                    }, {
                        'type': 'view',
                        'name': '核酸检测',
                        'url': 'https://www.wjx.cn/jq/81216464.aspx'
                    }, {
                        'type': 'miniprogram',
                        'name': '预约疫苗接种',
                        'url': 'https://app.cn2030.com/html/xiaochengxu.html',
                        'appid': 'wx2c7f0f3c30d99445',
                        'pagepath': 'tabs/tab_1/tab_1'
                    }, {
                        'type': 'view',
                        'name': '满意度调查',
                        'url': 'https://www.wjx.cn/jq/13633050.aspx'
                    }
                }
            }
        ]
    })
