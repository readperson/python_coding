import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from tools.random_number import *
from tools.base64_text import base64_text
from tools.headers import headers_header
from tools.mysql_insert.community_insert_mysql import commit_mysqlDB
import datetime


def community_data_capture():
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    nowTime = (datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S")
    url = "https://mobile-gate.611.com/api/CirlcleData"
    t = 24

    for i in range(24):
        minTime = (datetime.datetime.now() + datetime.timedelta(hours=-t)).strftime(
            "%Y-%m-%d %H:%M:%S")
        t = t - 1
        print("maxTime", nowTime, "minTime", minTime)
        data = {
            "minTime": str(minTime),
            "customValue": "",
            "maxTime": str(nowTime)}

        headers = {
            "deviceid": deviceid,
            "deviceaid": deviceaid,
            "requestRam": requestRam,
            "sign": sign,
            "lytime": lytime,
            "source": source
        }
        rep = requests.post(url=url, data=data, headers=headers)
        rep = json.loads(rep.text)
        # print(rep)
        for j in range(int(len(rep["data"]["list"]))):
            community_info = {}
            # 标题
            title = str(rep["data"]["list"][j]["displayDatas"][0]["title"])
            # 发布者者昵称
            nickName = str(rep["data"]["list"][j]["displayDatas"][0]["user"]["nickName"])
            headImageUrl = str(rep["data"]["list"][j]["displayDatas"][0]["user"]["headImageUrl"])
            contentId = str(rep["data"]["list"][j]["displayDatas"][0]["contentId"])
            # 发布时间
            pubTime = str(rep["data"]["list"][j]["displayDatas"][0]["pubTime"])
            pubTimeStr = str(rep["data"]["list"][j]["displayDatas"][0]["pubTimeStr"])
            # 标签
            srcName = str(rep["data"]["list"][j]["displayDatas"][0]["srcName"])
            # 副标题
            contentTxt = str(rep["data"]["list"][j]["displayDatas"][0]["contentTxt"])
            littleImg = str(rep["data"]["list"][j]["displayDatas"][0]["mediaList"][0]["littleImg"])
            # print(title, contentId, hitsCount, pubTime, pubTimeStr, srcName, contentTxt, littleImg)
            if int(len(contentTxt)) > 50:
                if int(len(littleImg)) > 0:
                    community_info["title"] = title.replace("乐鱼体育", "").replace("彩经", "")
                    print(title.replace("乐鱼体育", "").replace("彩经", ""), "现在时间:", nowTime, "发布时间：", pubTime)
                    community_info["nickName"] = nickName
                    community_info["HeadImgUrl"] = headImageUrl
                    channelIconPath = ""
                    community_info["channelIconPath"] = channelIconPath
                    community_info["contentId"] = contentId
                    hitsCount = str(random_number_likes())
                    community_info["hitsCount"] = hitsCount
                    community_info["pubTime"] = pubTime
                    community_info["pubTimeStr"] = pubTimeStr
                    community_info["srcName"] = srcName
                    contentTxt = contentTxt.replace("乐鱼体育", "").replace("彩经", "")
                    community_info["contentTxt"] = contentTxt

                    community_info["littleImg"] = littleImg
                    community_info["come_from"] = "乐鱼体育"
                    community_info["capture_time"] = (
                            datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
                    community_info["capture_type"] = "社区"

                    html_url = "https://mobile-gate.611.com/api/DetailDataInfo"
                    html_data = {"infoId": contentId, "publishDate": pubTime}

                    html_headers = {
                        "deviceid": deviceid,
                        "deviceaid": deviceaid,
                        "requestRam": requestRam,
                        "sign": sign,
                        "lytime": lytime,
                        "source": source
                    }
                    html_result = requests.post(url=html_url, data=html_data, headers=html_headers).text
                    html_result = json.loads(html_result)
                    # print(html_result)
                    htmlContent = ""
                    for cont_count in range(int(len(html_result["data"]["contentDatas"]))):
                        #
                        if "content" in html_result["data"]["contentDatas"][cont_count]:
                            content = str(html_result["data"]["contentDatas"][cont_count]["content"])
                            htmlContent = htmlContent + "<p>" + content + "</p></br>"
                        else:
                            htmlContent = html_result["data"]["contentDatas"][cont_count].setdefault("content", "")

                        if "icon" in html_result["data"]["contentDatas"][cont_count]:
                            icon_image = str(html_result["data"]["contentDatas"][cont_count]["icon"])
                            community_info["icon_image"] = icon_image

                    comment_url = "https://mobile-gate.611.com/api/DetailDataComnments"
                    comment_data = {"infoId": contentId, "publishDate": pubTime, "isHot": "false",
                                    "minTime": ""}

                    comment_headers = {
                        "deviceid": deviceid,
                        "deviceaid": deviceaid,
                        "requestRam": requestRam,
                        "sign": sign,
                        "lytime": lytime,
                        "source": source
                    }
                    comment_result = requests.post(url=comment_url, data=comment_data, headers=comment_headers).text
                    comment_result = json.loads(comment_result)
                    if "data" in comment_result:
                        comment_count = len(comment_result["data"])
                    else:
                        comment_count = 0
                        comment_result.setdefault("data", "")
                    community_info["comment_count"] = comment_count
                    comment_list = []
                    comment_counts = int(len(comment_result["data"]))
                    if comment_counts > 0:
                        print("     评论", comment_counts)
                    for community_count in range(comment_counts):
                        comment_dict = {}
                        id = comment_result["data"][community_count]["id"]
                        userId = comment_result["data"][community_count]["user"]["userId"]
                        headImageUrl = comment_result["data"][community_count]["user"]["headImageUrl"]
                        nickName = comment_result["data"][community_count]["user"]["nickName"]
                        postdate = comment_result["data"][community_count]["postdate"]
                        content = comment_result["data"][community_count]["content"]

                        comment_dict["id"] = id
                        comment_dict["userId"] = userId
                        comment_dict["headImageUrl"] = headImageUrl
                        comment_dict["nickName"] = nickName
                        comment_dict["postdate"] = postdate
                        comment_dict["content"] = base64_text(content)
                        comment_list.append(comment_dict)

                    community_info["comment"] = comment_list
                    community_info["htmlContent"] = htmlContent
                    commit_mysqlDB(contentId, title, nickName, hitsCount, pubTime, srcName, contentTxt, littleImg,
                                   channelIconPath, headImageUrl, icon_image, str(comment_list).replace("'", '"'))

                    print("组装成功的json:", str(community_info).replace("'", '"'))
                    print()


if __name__ == '__main__':
    community_data_capture()
