import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from tools.time_treatment import now_timestamp
from tools.time_treatment import now_time
import random
from tools.response_api import response_api


# 完美世界电竞 资讯
def e_sports_info():
    timestamp = now_timestamp()
    # print(timestamp)
    for page in range(5):
        page = page + 1
        url = "https://appactivity.wmpvp.com/steamcn/community/homepage/getData?sign=770e00f9567367df51cca950b0a60d17"
        data = {"appVersion": "1.4.6.46", "t": timestamp, "gameAbbr": "CSGO", "page": page,
                "deviceId": "dbf4e05c541f9ee9", "platform": "android"}
        data = json.dumps(data)
        # print("data", data)
        headers = {"platform": "android",
                   "t": "1606275164",
                   "appVersion": "1.4.6.46",
                   "gameType": "2",
                   "Content-Type": "application/json;charset=UTF-8",
                   "Content-Length": "121",
                   "Host": "appactivity.wmpvp.com",
                   "Connection": "close",
                   "Accept-Encoding": "gzip,deflate",
                   "User-Agent": "okhttp/3.12.6"
                   }

        result = requests.post(url=url, headers=headers, data=data).text
        result = json.loads(result)
        # print("result:::", result)
        result_count = int(len(result["data"]["newsList"]))
        for re_count in range(result_count):
            print("资讯共有", 5, "页,正在处理第", page, "页的第", re_count + 1, "条数据", "处理时间:", now_time())
            base = {}
            id = result["data"]["newsList"][re_count]["id"]
            gmtCreate = result["data"]["newsList"][re_count]["gmtCreate"]
            author = result["data"]["newsList"][re_count]["author"]
            pageViewCount = result["data"]["newsList"][re_count]["pageViewCount"]
            title = result["data"]["newsList"][re_count]["content"]["title"]
            summary = result["data"]["newsList"][re_count]["content"]["summary"]
            image = result["data"]["newsList"][re_count]["content"]["image"]
            detailed_info = result["data"]["newsList"][re_count]["newUrl"]
            url_info = result["data"]["newsList"][re_count]["url"]
            commentUrl = result["data"]["newsList"][re_count]["commentUrl"]
            identify = random.randint(1, 2)
            base["id"] = str(id)
            base["gmtCreate"] = gmtCreate
            base["author"] = author
            base["pageViewCount"] = pageViewCount
            base["title"] = title
            base["summary"] = summary
            base["image"] = image
            base["detailed_info"] = url_info
            base["identify"] = str(identify)
            base["commentUrl"] = commentUrl

            url = "/esports/save_esports_news"
            response_api(url, base)


if __name__ == '__main__':
    e_sports_info()
