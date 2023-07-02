# python 3.8
import base64
import hashlib
import hmac
import json
import os
import requests
import sys
import time
import urllib.parse


def sent_message(text: str, title: str, picUrl: str, messageUrl: str):
    secret = 'SEC3ff30c626bffa51c35844ff75934e5f3c22c98dd587cfa9485212625402ecf08'
    try:
        token = sys.argv[1]
    except:
        token = os.environ['DD_TOKEN']
        print('secret loss')
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print(timestamp)
    print(sign)
    url = "https://oapi.dingtalk.com/robot/send?access_token={2}&timestamp={0}&sign={1}".format(timestamp, sign, token)
    data = {
        "msgtype": "link",
        "link": {
            "text": text,
            "title": title,
            "picUrl": picUrl,
            "messageUrl": messageUrl
        }
    }
    headers = {"Content-Type": "application/json"}
    data = json.dumps(data)
    rsp = requests.post(url=url, data=data, headers=headers)
    print(rsp.json().get('errmsg'))


sent_message("通知\n" + "info", "title", "img", "url")
