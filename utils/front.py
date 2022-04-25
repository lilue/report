import json
import requests
from hashlib import md5
from report import settings
HOST_API = settings.FRONT_END['HOST']
TOKEN = settings.FRONT_END['TOKEN']


def splicing(body):
    str_param = body + TOKEN
    md = md5(str_param.encode("utf-8"))
    return md.hexdigest()


def post_ask(site, payload, s_str):
    url = HOST_API + site
    md5Str = splicing(s_str)
    payload['md5str'] = md5Str
    # print(payload)
    headers = {'content-Type': 'application/json', 'Accept': '*/*'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)
