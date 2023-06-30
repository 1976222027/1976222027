import datetime
import json
import requests

jiaban = [
    ["付海申"， "李学林"， "马洪印"]，
    ["李运琴"， "田青林"， "李晓欢"]，
    ["张志朋"， "任诘嘉"， "周福生"]，
    ["周广鹏"， "纪元"， "赵昱胜"]，
    ["卢超"， "刘新顺"]， []， []]


# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
# time.strptime()函数根据指定的格式把一个时间字符串解析为时间元组。
def getDays(str1, str2):
    date1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d")
    num = (date2 - date1).days
    return num


def doSort(time):
    countD = getDays('2023-7-3', time)
    zhou = countD // 7  # //取整
    index = countD % 7
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


def get_datas(my_time):
    name = doSort(my_time)
    # 返回钉钉模型数据，1:文本；
    if '马洪印' in name:
        mobie = '15732164757'
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



if __name__ == "__main__":
    dd_token = 'ba35e19ca18333d8efd8ff8da2535ab1915a2457997472c8f60e3578b694e269'
    my_data = get_datas(datetime.today().strftime("%Y-%m-%d"))
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    my_url = "https://oapi.dingtalk.com/robot/send?access_token="+dd_token
    ret = requests.post(url=my_url, data=json.dumps(my_data), headers=header)
    if ret.status_code == 200:
        print(ret.text)
