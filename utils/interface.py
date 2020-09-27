import requests
import json

host = 'http://127.0.0.1:8888/hohan/'


def encrypts(body, method='encrypt'):
    url = host + 'encrypt'
    post_data = {'body': body, 'method': method}
    response = requests.post(url=url, json=post_data)
    result = json.loads(response.text)
    print(result)
    return result


def card_api(params, method):
    url = host + 'health_card'
    params.update({'method': method})
    response = requests.post(url=url, json=params)
    result = json.loads(response.text)
    return result


def get_medical(params):
    response = requests.post(url=host, json=params)
    result = json.loads(response.text)
    return result['medical']


def get_birth(card):
    temp = card[6:14]
    y = temp[:4]
    m = temp[4:6]
    d = temp[6:8]
    birth = "{:s}-{:s}-{:s}".format(y, m, d)
    return birth


if __name__ == '__main__':
    # code = encrypts('440825199212101991')
    # print(code)
    # p = {'idCode': code, 'idCardTypeCode': '01'}
    # res = card_api(p, 'getPersonInfo')
    # print(res)
    p = {'name': '测试', 'idCode': '440825198502170050', 'address': '史蒂夫', 'birth': get_birth('440825198502170050'),
         'phone': '15876383959'}
    dd = get_medical(p)
    print(dd)
    # aa = get_birth('330106200503287127')
    # print(aa)
