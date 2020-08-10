import json
import requests
from report import settings

domain = settings.API_HOST
headers = {'content-Type': 'application/json', 'Accept': '*/*'}


def signApi(params):
    url = domain + 'sign'
    response = requests.post(url=url, data=json.dumps(params), headers=headers)
    return response


def encryptApi(params):
    url = domain + 'encrypt'
    response = requests.post(url=url, data=json.dumps(params), headers=headers)
    return response


def decryptApi(params):
    url = domain + 'deciphering'
    response = requests.post(url=url, data=json.dumps(params), headers=headers)
    return response


if __name__ == '__main__':
    raw1 = {"key": "F2D8D966CD3D47788449C19D5EF2081B", "mode": "SM3", "body": {
        "version": "V2.0.0",
        "nonceStr": "22444652459735737",
        "timestamp": "C46858AF978B7F4E4DDDB230E8B7996A",
        "appId": "60C90F3B796B41878B8D9C393E2B6329"
    }}
    raw2 = {
        "key": "F2D8D966CD3D47788449C19D5EF2081B",
        "params": "你猜我加密的是什么",
        "mode": "SM4/ECB/ZeroBytePadding"
    }
    raw3 = {
        "key": "F2D8D966CD3D47788449C19D5EF2081B",
        "params": "630FA60411547A471D1875A79C9A998D700BE4D3964D0CCE0B5FDDB37A823E2C",
        "mode": "SM4/ECB/ZeroBytePadding"
    }
    # res = signApi(raw1)
    # res = encryptApi(raw2)
    res = decryptApi(raw3)
    print(res.text)

# {
# 	"key": "F2D8D966CD3D47788449C19D5EF2081B",
# 	"mode": "SM3",
# 	"body": {
# 		"version": "V2.0.0",
# 		"nonceStr": "22444652459735737",
# 		"timestamp": "C46858AF978B7F4E4DDDB230E8B7996A",
# 		"appId": "60C90F3B796B41878B8D9C393E2B6329"
# 	}
# }
