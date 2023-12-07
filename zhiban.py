import datetime
import json
import os
import requests

jiaban = [
    ["周福生", "李晓欢"],
    ["付海申", "李学林", "马洪印"],
    ["李运琴", "田青林"],
    ["张志朋", "任诘嘉"],
    ["周广鹏", "赵昱胜"],
    ["纪元", "刘新顺"]
]


# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
# time.strptime()函数根据指定的格式把一个时间字符串解析为时间元组。
def getGapDays(str1, str2):
    date1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d")
    num = (date2 - date1).days
    return num


# 从2023-12-6开始，每周一三四为值班 按着顺序依次循环jiaban表

# 周1/3/4
def doSort(time):
    # 今天和初始天差几天
    countD = getGapDays('2023-7-3', time)
    zhou = countD // 7  # //取整
    index = countD % 7  # %取余
    if index < 5:
        if zhou > 4:
            zhou = zhou % 5
        if zhou != 0:
            # if index < zhou:
            #     index = index + (5 - zhou)
            # elif index == zhou:
            #     index = 0
            # else :
            #     index = index - zhou

            if index == 5 - zhou:
                index = 0
            elif index < 5 - zhou:
                index = index + zhou
            else:
                index = index - (5 - zhou)

    return "今日值班" + time + '\n' + str(jiaban[index])


def get_datas(today):
    # my_time = today.strftime('%Y-%m-%d')
    # name = doSort(my_time)
    name = getDateOfficer(today)
    # 返回钉钉模型数据，1:文本；
    if '马洪印' in name:
        mobie = os.environ['MOBIE']
    else:
        mobie = ''
    my_data = {
        "msgtype": "text",
        "text": {
            "content": "通知:" + "\n" + name + "\n"
        },
        "at": {
            "atMobiles": [
                mobie
            ],
            "isAtAll": False  # 这个参数为true好像是@所有人的意思
        }
    }
    return my_data


# 123 456 123 456
def getDateOfficer(current_date):
    week = [0, 2, 3]
    current_weekday = current_date.weekday()
    # 检查是否为周一、周三或周四
    if current_weekday in week:  # 周一是0，周三是2，周四是3
        day_of_week = ['周一','周二', '周三', '周四', '周五']
        # 只用于比较 不用关心时区
        start_date = datetime.date(2023, 12, 4)
        currentdate = datetime.date.today()
        delta = currentdate - start_date
        week_num = delta.days // 7
        index = week.index(current_date.weekday())
        # 0头周 1尾周
        if week_num % 2 != 0:
            index += 3
        day_officer = jiaban[index]
        return f"今天是{day_of_week[current_weekday]}，以下是今天的值班人员：{day_officer}"
    else:
        return "今天不是周一、周三或周四，不需要安排值班。"


if __name__ == "__main__":
    # 时区问题
    # SHA_TZ = datetime.timezone(
    #     datetime.timedelta(hours=8),
    #     name='Asia/Shanghai',
    # )
    # # 协调世界时
    # utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    # beijing_now = utc_now.astimezone(SHA_TZ)
    # today = beijing_now.date().strftime("%Y-%m-%d")

    now = datetime.datetime.utcnow()  # utc时间 因为服务器在国外的将不是北京时间
    bj_time = now + datetime.timedelta(hours=8)  # 直接加8，很傻瓜
    # today =datetime.datetime.today().strftime("%Y-%m-%d") #时区问题
    my_data = get_datas(bj_time)
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    dd_token = os.environ['TOKEN_DD']
    my_url = "https://oapi.dingtalk.com/robot/send?access_token=" + dd_token
    ret = requests.post(url=my_url, data=json.dumps(my_data), headers=header)
    if ret.status_code == 200:
        print(ret.text)
