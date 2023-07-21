"""
青龙脚本
mt论坛自动签到
添加变量mtluntan
账号密码用&隔开
例如账号：1234 密码：1111 则变量为1234&1111
定时规则: 0 0 * * *
"""
import json
import os
import re

import requests

# 设置ua
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
session = requests.session()

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


# 签到函数
def main(username, password):
    headers = {'User-Agent': ua}
    session.get(
        'https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login',
        headers=headers)
    chusihua = session.get(
        'https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login',
        headers=headers)
    # print(re.findall('loginhash=(.*?)">', chusihua.text))
    loginhash = re.findall('loginhash=(.*?)">', chusihua.text)[0]
    formhash = re.findall('formhash" value="(.*?)".*? />', chusihua.text)[0]
    denurl = f'https://bbs.binmt.cc/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash={loginhash}&inajax=1'
    data = {'formhash': formhash, 'referer': 'https://bbs.binmt.cc/forum.php', 'loginfield': 'username',
            'username': username, 'password': password, 'questionid': '0', 'answer': '', }
    denlu = session.post(headers=headers, url=denurl, data=data).text
    print(denlu)
    if '欢迎您回来' in denlu or '登录成功' in denlu:
        # 获取分组、名字
        # fzmz = re.findall('欢迎您回来，(.*?)，现在', denlu)[0]
        # print(f'{fzmz}：登录成功')
        # 获取formhash
        zbqd = session.get('https://bbs.binmt.cc/k_misign-sign.html', headers=headers).text
        formhash = re.findall('formhash" value="(.*?)".*? />', zbqd)[0]
        # 签到
        qdurl = f'https://bbs.binmt.cc/plugin.php?id=k_misign:sign&operation=qiandao&format=text&formhash={formhash}'
        qd = session.get(url=qdurl, headers=headers).text
        qdyz = re.findall('<root><(.*?)</root>', qd)
        print(qdyz)
        # login_info = re.findall('欢迎您回来，(.*?)，现在', denlu)[0].strip()
        sign_info = re.findall('<root><(.*?)</root>', qd)[0].strip()
        pushplus_notify('MT论坛签到通知', f'签到信息：{sign_info}')
    else:
        print('登录失败')
        pushplus_notify('MT论坛登录失败', '登录失败')


if __name__ == '__main__':
    # mtluntan = os.getenv("MT_BBS")
    mtluntan = os.environ["MT_BBS"]
    # 从环境变量中读取账号密码
    if mtluntan is not None:
        username, password = mtluntan.split('&')
        main(username, password)
    else:
        print('未设置MT论坛账号密码')
