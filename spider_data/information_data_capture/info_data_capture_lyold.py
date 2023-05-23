import sys
sys.path.append("/opt/data_captureAPP")
import json
import requests
from tools.get_to_ken import *
from tools.random_number import *
import datetime


def info_data_capture_ly():
    nowTime = (datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S")
    t_m = 24
    for t in range(24):
        minTime = (datetime.datetime.now() + datetime.timedelta(hours=-t_m)).strftime("%Y-%m-%d %H:%M:%S")
        t_m = t_m - 1
        print(nowTime, minTime)
        access = get_to_ken()
        url = "https://mobile-gate.611.com/api/RecommendData"
        headers = {
            "deviceid": "1217bd0c9497d7c624aee3d2b2ad13a6",
            "deviceaid": "1217bd0c9497d7c624aee3d2b2ad13a6",
            "requestRam": "1604489294",
            "sign": "aa70276fbe3e35b7b1c848f3ef4b8c42",
            "lytime": "2020-11-04 07:28:14",
            "source": "1"
        }
        data = {
            "tabId": "ad2f0237-e0db-4e89-af10-88e7919459b4",
            "isFirst": "false",
            "isRefresh": "false",
            "minTime": str(minTime),
            "maxTime": str(nowTime),
            "customValue": ""}
        # data = {
        #     "tabId": "d2f0237-e0db-4e89-ad2f0237-e0db-4e89-af10-88e7919459b4-88e7919459b4",
        #     "isFirst": "false",
        #     "isRefresh": "false",
        #     "minTime": "2020-10-16 " + str(t) + ":12:34",
        #     "maxtime": "2020-10-22 10:31:35",
        #     "customValue": ""}
        rep = requests.post(url=url, headers=headers, data=data).text
        rep = json.loads(rep)
        print(rep)
        for i in range(int(len(rep["data"]["list"]))):
            info_capture = {}
            articleTitle = str(rep["data"]["list"][i]["displayDatas"][0]["title"])
            articleId = str(rep["data"]["list"][i]["displayDatas"][0]["contentId"])
            articleViewCount = random_number_readings()
            articleGoodCount = random_number_likes()
            tagName = str(rep["data"]["list"][i]["displayDatas"][0]["contentTag"])
            publishTime = str(rep["data"]["list"][i]["displayDatas"][0]["pubTime"])
            imageStr = str(rep["data"]["list"][i]["displayDatas"][0]["iconUrl"])
            publishTimeStr = "1小时前"
            # articleContent = str(rep["data"]["list"][i]["displayDatas"][0]["contentTxt"])
            url_c = "https://mobile-gate.611.com/api/DetailDataInfo"
            headers_c = {
                "deviceid": "1217bd0c9497d7c624aee3d2b2ad13a6",
                "deviceaid": "1217bd0c9497d7c624aee3d2b2ad13a6",
                "requestRam": "1603786621",
                "sign": "d6713f0dfe7b868124756ccccfcc7cdf",
                "lytime": "2020-10-27 04:17:01",
                "source": "1"
            }
            data_c = {
                "infoId": articleId,
                "publishDate": publishTime}
            rep1 = requests.post(url=url_c, headers=headers_c, data=data_c).text
            rep1 = json.loads(rep1)
            articleArthurNickname = rep1["data"]["headList"]["user"]["nickName"]
            HeadImgUrl = rep1["data"]["headList"]["user"]["headImageUrl"]

            articleContent=""
            for cont_count in range(int(len(rep1["data"]["contentDatas"]))):
                #
                if "content" in rep1["data"]["contentDatas"][cont_count]:
                    content = str(rep1["data"]["contentDatas"][cont_count]["content"])
                    articleContent = articleContent +"<p>"+content+"</p></br>"
                else:
                    content = rep1["data"]["contentDatas"][cont_count].setdefault("content","")




            if int(len(articleContent)) > 50:
                if int(len(imageStr)) > 0:
                    info_capture["articleTitle"] = articleTitle.replace("乐鱼", "**").replace("彩经", "")
                    info_capture["articleId"] = articleId
                    info_capture["articleViewCount"] = str(articleViewCount)
                    info_capture["articleGoodCount"] = str(articleGoodCount)
                    info_capture["articleArthurNickname"] = articleArthurNickname
                    info_capture["HeadImgUrl"] = HeadImgUrl
                    info_capture["tagName"] = tagName
                    info_capture["publishTime"] = publishTime
                    info_capture["publishTimeStr"] = publishTimeStr
                    info_capture["imageStr"] = imageStr
                    info_capture["come_from"] = "乐鱼体育"
                    info_capture["capture_time"] = nowTime
                    info_capture["capture_type"] = "足球"
                    # https://mobile-gate.611.com/api/DetailDataInfo
                    #
                    info_capture["articleContent"] = articleContent.replace("乐鱼", "**").replace("彩经", "")
                    print("组装成的json数据:", str(info_capture).replace("'", '"'))
                    comm_url = "http://47.114.6.60/news/save_news"
                    info_capture_json = json.dumps(info_capture)

                    comm_headers = {"Content-Type": "application/json;charset=utf-8",
                                    "Authorization": "Bearer " + access}
                    print("请求url:", comm_url)
                    print("请求头:", comm_headers)
                    print("请求数据:", info_capture_json)
                    result = requests.post(url=comm_url, data=info_capture_json, headers=comm_headers)
                    print("请求返回状态码：", result.status_code)
                    print(result.text)
                    print("")
            # print(rep1)


if __name__ == '__main__':
    info_data_capture_ly()
