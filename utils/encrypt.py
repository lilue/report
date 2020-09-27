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


def encrypts(body, method='encrypt'):
    url = domain + method
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
def card_common_api(params, method):
    sign = head_sign_splice()
    head_sign = signs(sign)
    body = {"appMode": "5", "orgCode": org_code, "appRecordNo": app_record_no}
    body.update(params)
    body_sign = signs(body)
    head = {"method": method, "headSign": head_sign, "bodySign": body_sign,
            "signMode": sign_mode, "encryptMode": encrypt_mode, "body": body}
    sign.update(head)
    response = requests.post(url=api_hosts, data=json.dumps(sign), headers=headers)
    return json.loads(response.text)


if __name__ == '__main__':
    # res = common_api('01', '440825199503170030', 'queryIfHasRegistered')
    # print(res)
    # print(res['datas']['parameters'])
    # res = common_api('01', '440825199212101991', 'queryIfHasRegistered')
    # print(res)
    # print(res['datas']['parameters'])

    # print(int(time.time()))
    code = encrypts('440825199212101991')
    # p = {'idCode': code, 'idCardTypeCode': '01'}
    # p = {'idCode': 'A80F4714F85762E636F6901B4F76F7F8BA5959655252F2AE5989B2EE77401260', 'idCardTypeCode': '01',
    #      'personnelType': '1',
    #      'name': 'BCD7B45A26485CC292ABB7F0522F7A10', 'nation': '01'}
    # register_result = card_common_api(p, 'createVmcardQRcode')
    # print(register_result)
    p = {'idCode': code, 'idCardTypeCode': '01'}
    res = card_common_api(p, 'getPersonInfo')
    # print(int(time.time()))
    # res = card_common_api(p, 'getPersonInfo')
    print(res)
    # print(res['datas']['erhcCardNo'])

    # res = no_common_api('AC1A63FE55BE66264027A86CF21C25E049E85BCEDB70C901', 'getPersonInfo')
    # print(res)
