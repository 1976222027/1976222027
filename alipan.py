import os

import requests
import json


# 第一步，在电脑上获取token的办法。
# 打开阿里云盘网页版，打开控制台输入 JSON.parse(localStorage.getItem('token')).refresh_token 回车


# pushplus推送函数
def pushplus_notify(title, content):
    PUSH_PLUS_TOKEN = '800033ca79c142b3b5eda19aa011612d'  # 填入从pushplus官网申请的token字符串
    PUSH_PLUS_USER = ''  # 填入在pushplus官网新增的群组编码或个人用户的user字符串，可以不填。

    data = {
        "token": PUSH_PLUS_TOKEN,
        "user": PUSH_PLUS_USER,
        "title": title,
        "content": content
    }
    url = 'http://www.pushplus.plus/send'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, data=json.dumps(data), headers=headers)
    return response.text


def AliyunDrive():
    # 每月过期定期修改
    # token = os.environ["ALI_YUNPAN"]
    token = 'cd514b6081264980abaa1f4966f3bbc0'
    # 'JSON.parse(localStorage.getItem('token')).refresh_token'
    header = {
        'Content-Type': "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
    }

    url_page = 'https://auth.aliyundrive.com/v2/account/token'
    date = {'grant_type': 'refresh_token', "refresh_token": token}
    rep = requests.post(url=url_page, headers=header,
                        data=json.dumps(date)).content
    print('阿里云盘签到token：' + token)

    result = json.loads(rep)
    # print(result)
    access_token = result['access_token']
    phone = result['user_name']

    print('阿里云盘签到access_token：' + access_token)

    access_token2 = 'Bearer ' + access_token
    header2 = {
        'Authorization': access_token2,
        'Content-Type': "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
    }

    # date = {"_rx-s": "mobile"}
    # url_page = 'https://member.aliyundrive.com/v1/activity/sign_in_list'
    date = {'isReward': False}
    url_page = 'https://member.aliyundrive.com/v2/activity/sign_in_list?_rx-s=mobile'
    rep2 = requests.post(url=url_page, headers=header2,
                         data=json.dumps(date)).content
    result = json.loads(rep2)
    # print(result)
    signInCount = result['result']['signInCount']
    print('阿里云盘签到天数：' + str(signInCount) + "天")
    currentSignInfo = result["result"]["signInInfos"][signInCount - 1]
    signInDay = currentSignInfo["day"]
    for reward in currentSignInfo["rewards"]:
        if reward["status"] == 'finished':
            if reward['type'] == 'dailySignIn':
                try:
                    date = {"signInDay": signInDay}
                    url_page = 'https://member.aliyundrive.com/v1/activity/sign_in_reward?_rx-s=mobile'
                    rep3 = requests.post(url=url_page, headers=header2,
                                         data=json.dumps(date)).content
                    result = json.loads(rep3)
                    print(result)
                except:
                    print("gg")
            elif reward['type'] == 'dailyTask':
                try:
                    date = {"signInDay": signInCount}
                    url_page = 'https://member.aliyundrive.com/v2/activity/sign_in_task_reward?_rx-s=mobile'
                    rep3 = requests.post(url=url_page, headers=header2,
                                         data=json.dumps(date)).content
                    result = json.loads(rep3)
                    print(result)
                except:
                    print("gg")
        elif reward["status"] == 'unfinished':
            print("任务未完成")
        elif reward["status"] == 'end':
            print("任务已结束")
        else:
            print('第${signInDay}天领取奖励:reward.name')

    date = {"signInDay": signInCount}
    # url_page = 'https://member.aliyundrive.com/v1/activity/sign_in_reward?_rx-s=mobile'
    url_page = 'https://member.aliyundrive.com/v2/activity/sign_in_task_reward?_rx-s=mobile'
    rep3 = requests.post(url=url_page, headers=header2,
                         data=json.dumps(date)).content
    result = json.loads(rep3)
    print(result)
    # name = result["result"]["name"]
    # description = result["result"]["description"]

    res = "签到成功, 本月累计签到" + str(signInCount) + "天"
    res2 = result['message'] + ",本次签到获得"  #+ name + "," + description
    return res + "\n" + res2


value = AliyunDrive()
print(value)
if value is not None:
    pushplus_notify('阿里云盘签到通知', f'签到信息：{value}')
