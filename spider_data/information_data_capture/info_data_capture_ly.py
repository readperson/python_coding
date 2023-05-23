import sys

sys.path.append("/opt/data_captureAPP")
import json
import requests
from tools.get_to_ken import *
from tools.random_number import *
from tools.headers import headers_header
import datetime
from tools.base64_text import text_conversion_base64
from tools.response_api import response_api


def info_data_capture_ly():
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    nowTime = (datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S")
    t_m = 24
    for t in range(24):
        minTime = (datetime.datetime.now() + datetime.timedelta(hours=-t_m)).strftime("%Y-%m-%d %H:%M:%S")
        t_m = t_m - 1

        url = "https://mobile-gate.611.com/api/RecommendData"
        headers = {
            "deviceid": deviceid,
            "deviceaid": deviceaid,
            "requestRam": requestRam,
            "sign": sign,
            "lytime": lytime,
            "source": source
        }
        data = {
            "tabId": "ad2f0237-e0db-4e89-af10-88e7919459b4",
            "isFirst": "false",
            "isRefresh": "false",
            "minTime": str(minTime),
            "maxTime": str(nowTime),
            "customValue": ""}
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
            url_c = "https://mobile-gate.611.com/api/DetailDataInfo"
            headers_c = {
                "deviceid": deviceid,
                "deviceaid": deviceaid,
                "requestRam": requestRam,
                "sign": sign,
                "lytime": lytime,
                "source": source
            }
            data_c = {
                "infoId": articleId,
                "publishDate": publishTime}
            rep1 = requests.post(url=url_c, headers=headers_c, data=data_c).text
            rep1 = json.loads(rep1)
            articleArthurNickname = rep1["data"]["headList"]["user"]["nickName"]
            HeadImgUrl = rep1["data"]["headList"]["user"]["headImageUrl"]
            # 副标题
            articleContent = ""
            for cont_count in range(int(len(rep1["data"]["contentDatas"]))):
                #
                if "content" in rep1["data"]["contentDatas"][cont_count]:
                    content = str(rep1["data"]["contentDatas"][cont_count]["content"])
                    articleContent = articleContent + "<p>" + content + "</p></br>"
                else:
                    content = rep1["data"]["contentDatas"][cont_count].setdefault("content", "")
            # 正文内容
            htmlContent = str(rep1["data"]["headList"]["htmlContent"]).replace("\n", "</br>").replace("乐鱼",
                                                                                                      "**").replace(
                "彩经", "")

            if int(len(articleContent)) > 50:
                if int(len(imageStr)) > 0:
                    info_capture["come_from"] = "乐鱼体育"
                    info_capture["capture_time"] = nowTime
                    info_capture["capture_type"] = "足球"
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
                    articleContent = articleContent.replace("乐鱼", "**").replace("彩经", "")
                    info_capture["articleContent"] = articleContent
                    info_capture["htmlContent"] = text_conversion_base64(htmlContent)
                    print(nowTime, minTime, publishTime)
                    # print("组装成的json数据:", str(info_capture).replace("'", '"'))
                    print("")
                    url_tj = "/news/save_news"
                    response_api(url_tj, info_capture)


if __name__ == '__main__':
    info_data_capture_ly()
