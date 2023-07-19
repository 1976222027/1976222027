#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：注意token失效情况  和企业微信可信ip  https://work.weixin.qq.com/wework_admin/frame#/apps/modApiApp/5629501753576427
@file    ：玩安卓 每日打卡
@IDE     ：PyCharm
@AuThor  ：海绵的烂笔头
@date    ：2023-07-14 12:55
'''
import json
import os
import requests

# =========================================以下为工控家人园打卡程序，如果CK失效，只需要替换这部分内容=========================================
cookies = {
    'Hm_lvt_90501e13a75bb5eb3d067166e8d2cad8': '1687682924',  # 20230625
    'loginUserName': 'myname',
    'token_pass': 'c2363be327e6353fb6ddc7426b8f1bcc',
    'loginUserName_wanandroid_com': 'myname',
    'token_pass_wanandroid_com': 'c2363be327e6353fb6ddc7426b8f1bcc',
    'JSESSIONID': 'B2125EE1C7FE4F82CD903806D5C2B0D1',
    'Hm_lpvt_90501e13a75bb5eb3d067166e8d2cad8': '1689747788',  # 2023-07-19
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_90501e13a75bb5eb3d067166e8d2cad8=1687682924; loginUserName=myname; token_pass=c2363be327e6353fb6ddc7426b8f1bcc; loginUserName_wanandroid_com=myname; token_pass_wanandroid_com=c2363be327e6353fb6ddc7426b8f1bcc; JSESSIONID=B2125EE1C7FE4F82CD903806D5C2B0D1; Hm_lpvt_90501e13a75bb5eb3d067166e8d2cad8=1689747788',
    'Referer': 'https://www.wanandroid.com/blog/show/2',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://www.wanandroid.com/lg/coin/userinfo/json', cookies=cookies, headers=headers)
# =======================================对文件进行编码处理=====================================================
# response.encoding = 'gbk'
# =======================================以下为对打印内容的处理，只保留文字=====================================================
res = response.text
print(res)
code = json.loads(res)['errorCode']
if code == 0:
    t = "打卡成功:" + res
else:
    t = "打卡失败:" + res
# ==============================================以下为企业微信推送程序=======================================================
CORP_ID = os.environ['WX_CORP_ID']  # 企业ID
SECRET = os.environ['WX_CORP_SECRET']  # 应用secret
WX_ROBOT = os.environ['WX_ROBOT']  # 机器人


class WeChatPub:
    s = requests.session()

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
                        "title": "打卡通知",
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


if __name__ == "__main__":
    wechat = WeChatPub(1)
    image_url = "https://wework.qpic.cn/wwpic/789412_-8Pbh00NQZqwdjE_1660630201/0"  # 图片的URL
    wechat.send_msg(f"注意！{t}", image_url)
