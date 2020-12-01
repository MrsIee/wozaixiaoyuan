import json
import logging
import requests, time, random
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Xiao:
    def __init__(self):
        # Token 列表
        self.tokenArray = [""]
        self.tokenName = ["某某某"]
        # 喵提醒通知
        self.notifyToken = '****'
        self.threeApi = "https://student.wozaixiaoyuan.com/heat/save.json"
        self.heathApi = "https://student.wozaixiaoyuan.com/health/save.json"
        self.headers = {
            "Host": "student.wozaixiaoyuan.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Referer": "https://servicewechat.com/wxce6d08f781975d91/147/page-frame.html",
            "token": "",
            "Content-Length": "360",
        }
        self.threeData = {
            "answers": '["0"]',
            "seq": self.get_seq(),
            "temperature": self.get_random_temprature(),
            "latitude": "",
            "longitude": "",
            "country": "中国",
            "city": "**市",
            "district": "**区",
            "province": "**省",
            "township": "***街道",
            "street": "***路",
        }
        self.heathData = {
            "answers": '["0"]',
            "date": self.get_date_str(),
            "id": "*****",
            "seq": "0",
            "latitude": "",
            "longitude": "",
            "country": "中国",
            "city": "**市",
            "district": "**区",
            "province": "**省",
            "township": "**街道",
            "street": "***路",
            "titles": [
                {
                    "healthOptions": [
                        {
                            "id": "0",
                            "select": 1,
                            "option": "无下列情况,身体健康",
                            "seq": 0,
                            "type": 0
                        }
                    ]
                }
            ]
        }

    #获取年-月-日
    def get_date_str(self):
        now = datetime.datetime.now()
        year = str(int(now.strftime('%Y')))
        month = str(int(now.strftime('%m')))
        day = str(int(now.strftime('%d')))
        return str(year + '-' + month + '-' + day)


    # 获取随机体温
    def get_random_temprature(self):
        random.seed(time.ctime())
        return "{:.1f}".format(random.uniform(36.2, 36.7))

    # seq的1,2,3代表着早，中，晚
    def get_seq(self):
        current_hour = datetime.datetime.now()
        current_hour = current_hour.hour
        print(current_hour)
        if 0 <= current_hour <= 8:
            return "1"
        elif 11 <= current_hour < 15:
            return "2"
        elif 17 <= current_hour < 21:
            return "3"
        else:
            return 1


    def run(self):
        num = 0
        for i in self.tokenArray:
            self.headers["token"] = i
            print("Token:" + self.headers["token"])
            # 格式化成2016-03-20 11:45:39形式
            print("当前时间", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            res = requests.post(self.threeApi, headers=self.headers, data=self.threeData).json()
            time.sleep(1)
            # print(self.heathData)
            res2 = requests.post(self.heathApi, headers=self.headers, data=self.heathData).json()
            time.sleep(1)

            print(res)
            print(res2)

            # randomstr = str(random.randint(1, 100))
            # "text": "Token" + randomstr + '\n' + self.tokenName[num] +self.headers["token"] + '\n' + json.dumps(res, ensure_ascii=False),

            status1 = str(res)[9]
            status2 = str(res2)[9]
            status1 = 'success' if status1 == '0' else 'fail'
            status2 = 'success' if status2 == "0" else 'fail'

            print(status1)
            print(status2)
            msg = {
                "id": self.notifyToken,
                "text": "日检:" + status1 + '\n' + "健康:" + status2,
                "type": "json"
            }
            requests.post("http://miaotixing.com/trigger", data=msg)
            num = num + 1
        #     global sum_msg = sum_msg + msg
        # requests.post("http://miaotixing.com/trigger", data=sum_msg)
        return True


if __name__ == "__main__":
    Xiao().run()


def main_handler(event, context):
    logger.info('got event{}'.format(event))
    return Xiao().run()
