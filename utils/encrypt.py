import json
import requests
import time
from report import settings

domain = settings.API_HOST
api_hosts = domain + 'do'
headers = {'content-Type': 'application/json', 'Accept': '*/*'}


def aesApi(method, temp):
    url = domain + method
    # sign 签名接口
    # encrypt 加密接口
    # deciphering 解密接口
    if method == 'sign':
        params = {"key": settings.API_KEY, "mode": settings.API_SIGN_MODE, "body": temp}
    else:
        params = {"key": settings.API_KEY, "mode": settings.API_ENCRYPT_MODE, "params": str(temp)}
    try:
        response = requests.post(url=url, data=json.dumps(params), headers=headers)
        response = json.loads(response.text)
        return response['result']
    except Exception as e:
        print(str(e))
        return 'None'


# 头部信息拼接
def head_sign_splice():
    time_stamp = int(time.time())
    time_stamp = aesApi('encrypt', str(time_stamp))
    sign = {"appId": settings.API_APP_ID,
            "timestamp": time_stamp,
            "nonceStr": settings.API_NONCE_STR,
            "version": settings.API_VERSION}
    return sign
    pass


# 通用的api接口，传入证件类型，证件号码，请求方法调用接口
def common_api(card_type, card_no, method):
    sign = head_sign_splice()
    head_sign = aesApi('sign', sign)
    idCode = aesApi('encrypt', card_no)
    body = {"idCode": idCode, "idCardTypeCode": card_type, "appMode": "5", "orgCode": settings.API_ORG_CODE,
            "appRecordNo": settings.API_APP_RECORD_NO}
    body_sign = aesApi('sign', body)
    # method 参数解释
    # 查询账户是否注册————queryIfHasRegistered
    # 个人信息查询————getPersonInfo
    head = {"method": method, "headSign": head_sign, "bodySign": body_sign,
            "signMode": settings.API_SIGN_MODE, "encryptMode": settings.API_ENCRYPT_MODE, "body": body}
    sign.update(head)
    response = requests.post(url=api_hosts, data=json.dumps(sign), headers=headers)
    return json.loads(response.text)


def create_api(card_type, card_no, name, phone):
    sign = head_sign_splice()
    head_sign = aesApi('sign', sign)
    idCode = aesApi('encrypt', card_no)
    name = aesApi('encrypt', name)
    phone = aesApi('encrypt', phone)
    body = {"name": name, "idCode": idCode, "idCardTypeCode": card_type, "nation": "01", "phone": phone}
    pass


if __name__ == '__main__':
    # res = common_api('01', '440825199503170030', 'queryIfHasRegistered')
    # print(res)
    # print(res['datas']['parameters'])
    # res = common_api('01', '440825199212101991', 'queryIfHasRegistered')
    # print(res)
    # print(res['datas']['parameters'])
    res = common_api('01', '440825199212101991', 'getPersonInfo')
    print(res)
    print(res['datas']['erhcCardNo'])
