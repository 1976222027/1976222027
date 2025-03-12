import hashlib
import hmac
import json
import os
import time

import requests


# 签到
# ==============================================以下为企业微信推送程序=======================================================


class WeChatPub:
    s = requests.session()
    token = ''

    def __init__(self, tp=0):
        if tp == 0:
            CORP_ID = os.environ['WX_CORP_ID']  # 企业ID
            SECRET = os.environ['WX_CORP_SECRET']  # 应用secret
            self.token = self.get_token(CORP_ID, SECRET)

    def get_token(self, CORP_ID, SECRET):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={SECRET}"
        rep1 = self.s.get(url)
        if rep1.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep1.content)['access_token']

    def send_msg(self, content, image_url):
        if len(self.token) == 0:
            WX_ROBOT = os.environ['WX_ROBOT']
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + WX_ROBOT
        else:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        #
        header2 = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "@all",  # MaHongYin|mhy
            "toparty": "1",
            "totag": "TagID1 | TagID2",
            "msgtype": "news",
            "agentid": 1000002,
            "news": {
                "articles": [
                    {
                        "title": "相加签到通知",
                        "description": content,
                        "url": "URL",
                        "picurl": image_url
                    }
                ]
            },
            "safe": 0
        }
        rep2 = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header2)
        if rep2.status_code == 200:
            print('消息已发送！\n' + rep2.text)
            return json.loads(rep2.content)
        print("request failed.")
        return

def calculate_md5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest().lower()


def calculate_signature(key, data):
    # 使用hmac模块，将key和data进行sha256加密，并返回加密后的十六进制字符串
    signature = hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()
    # 返回签名
    return signature

if __name__ == '__main__':
    host = 'iios.bxguwen.com'
    # secret = calculate_md5("xxxxx") #'63add3a71874e8200be66b14c826ae96'
    token = os.environ['XJTOKEN']
    #'6131376237306365626263663432616362303863376464376565386366653965'
    # 接口好像没有验证 secret, 只是定期更新token
    header = {
        'Host': host,
        # 'x-auth-key': str(int(time.time())),
        # 'x-auth-secret': secret,
        'Content-Type': "application/x-www-form-urlencoded",
        'User-Agent': 'Dio/4.1.8 Android',
        'Cookie': f'xxx_api_auth={token}; path=/'
    }

    url_page = "https://"+host + '/ucp/task/sign'

    rep = requests.post(url=url_page, headers=header)
    result = rep.text.encode('utf-8').decode('unicode_escape')
    print('相加签到token：' + result)

    # wechat = WeChatPub(1)
    # image_url = "https://wework.qpic.cn/wwpic/789412_-8Pbh00NQZqwdjE_1660630201/0"  # 图片的URL
    # wechat.send_msg(f"注意！{result}", image_url)

if __name__ == '__main3__':
    host = 'n15mo67l5mfd.vergissmeinnicht.xyz'
    url_page = "https://" + host + '/ucp/task/sign'
    time1 = '1741580114'
    print("d801f191f32b30f48a330c64c9409d9d")
    # 不知算法.....
    print(calculate_md5(url_page+"6131376237306365626263663432616362303863376464376565386366653965"+time1))