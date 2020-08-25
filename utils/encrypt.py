import json
import requests
import time
from report import settings

domain = settings.API_HOST
api_hosts = domain + 'do'
headers = {'content-Type': 'application/json', 'Accept': '*/*'}
key = settings.API_KEY
app_id = settings.API_APP_ID
nonce_str = settings.API_NONCE_STR
api_version = settings.API_VERSION
org_code = settings.API_ORG_CODE
app_record_no = settings.API_APP_RECORD_NO
sign_mode = settings.API_SIGN_MODE
encrypt_mode = settings.API_ENCRYPT_MODE


# def aesApi(method, temp):
#     url = domain + method
#     # sign 签名接口
#     # encrypt 加密接口
#     # deciphering 解密接口
#     if method == 'sign':
#         params = {"key": key, "mode": sign_mode, "body": temp}
#     else:
#         params = {"key": key, "mode": encrypt_mode, "params": str(temp)}
#     try:
#         response = requests.post(url=url, data=json.dumps(params), headers=headers)
#         response = json.loads(response.text)
#         return response['result']
#     except Exception as e:
#         print(str(e))
#         return 'None'


def signs(body):
    url = domain + 'sign'
    params = {"key": key, "mode": sign_mode, "body": body}
    try:
        response = requests.post(url=url, data=json.dumps(params), headers=headers)
        response = json.loads(response.text)
        return response['result']
    except Exception as e:
        print(str(e))
        return 'None'


def encrypts(body):
    url = domain + 'encrypt'
    params = {"key": key, "mode": encrypt_mode, "params": str(body)}
    try:
        response = requests.post(url=url, data=json.dumps(params), headers=headers)
        response = json.loads(response.text)
        return response['result']
    except Exception as e:
        print(str(e))
        return 'None'
    pass


# 头部信息拼接
def head_sign_splice():
    time_stamp = int(time.time())
    time_stamp = signs(str(time_stamp))
    sign = {"appId": app_id,
            "timestamp": time_stamp,
            "nonceStr": nonce_str,
            "version": api_version}
    return sign
    pass


# 传入证件类型，证件号码，请求方法调用接口
def card_common_api(card_type, card_no, method):
    sign = head_sign_splice()
    head_sign = signs(sign)
    idCode = encrypts(card_no)
    body = {"idCode": idCode, "idCardTypeCode": card_type, "appMode": "5", "orgCode": org_code,
            "appRecordNo": app_record_no}
    body_sign = signs(body)
    # method 参数解释
    # 查询账户是否注册————queryIfHasRegistered
    # 个人信息查询————getPersonInfo
    head = {"method": method, "headSign": head_sign, "bodySign": body_sign,
            "signMode": sign_mode, "encryptMode": encrypt_mode, "body": body}
    sign.update(head)
    response = requests.post(url=api_hosts, data=json.dumps(sign), headers=headers)
    return json.loads(response.text)


def no_common_api(no, method):
    sign = head_sign_splice()
    head_sign = signs(sign)
    body = {"erhcCardNo": no, "appMode": "5", "orgCode": org_code,
            "appRecordNo": app_record_no}
    body_sign = signs(body)
    head = {"method": method, "headSign": head_sign, "bodySign": body_sign,
            "signMode": sign_mode, "encryptMode": encrypt_mode, "body": body}
    sign.update(head)
    response = requests.post(url=api_hosts, data=json.dumps(sign), headers=headers)
    return json.loads(response.text)
    pass


# def create_api(card_type, card_no, name, phone):
#     sign = head_sign_splice()
#     head_sign = aesApi('sign', sign)
#     idCode = aesApi('encrypt', card_no)
#     name = aesApi('encrypt', name)
#     phone = aesApi('encrypt', phone)
#     body = {"name": name, "idCode": idCode, "idCardTypeCode": card_type, "nation": "01", "phone": phone}
#     pass


if __name__ == '__main__':
    # res = common_api('01', '440825199503170030', 'queryIfHasRegistered')
    # print(res)
    # print(res['datas']['parameters'])
    # res = common_api('01', '440825199212101991', 'queryIfHasRegistered')
    # print(res)
    # print(res['datas']['parameters'])

    # print(int(time.time()))
    # res = card_common_api('01', '440825199212101991', 'getPersonInfo')
    # print(int(time.time()))
    # print(res)
    # print(res['datas']['erhcCardNo'])

    res = no_common_api('AC1A63FE55BE66264027A86CF21C25E049E85BCEDB70C901', 'getPersonInfo')
    print(res)
