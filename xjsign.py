import json
import os

import requests


# 签到
# ==============================================以下为企业微信推送程序=======================================================
CORP_ID = os.environ['WX_CORP_ID']  # 企业ID
SECRET = os.environ['WX_CORP_SECRET']  # 应用secret
WX_ROBOT = os.environ['WX_ROBOT']  # 机器人


class WeChatPub:

    s = requests.session()
    token = ''

    def __init__(self, tp=0):
        if tp == 0:
            self.token = self.get_token()

    def get_token(self):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={SECRET}"
        rep = self.s.get(url)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)['access_token']

    def send_msg(self, content, image_url):
        if len(self.token) == 0:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + WX_ROBOT
        else:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        #
        header = {
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
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code == 200:
            print('消息已发送！\n' + rep.text)
            return json.loads(rep.content)
        print("request failed.")
        return


if __name__ == '__main__':
    header = {
        'Content-Type': "application/x-www-form-urlencoded",
        'User-Agent': 'Dio/3.8.3 Android',
        'Cookie': 'xxx_api_auth=3630623535393938363162356332313134386632353164316433666230363964; path=/'
    }
    url_page = 'https://iios.bxguwen.com/ucp/task/sign'
    rep = requests.post(url=url_page, headers=header)
    result = rep.text.encode('utf-8').decode('unicode_escape')
    print('相加签到token：' + result)

    wechat = WeChatPub(1)
    image_url = "https://wework.qpic.cn/wwpic/789412_-8Pbh00NQZqwdjE_1660630201/0"  # 图片的URL
    wechat.send_msg(f"注意！{result}", image_url)
