import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
import random
import datetime
from tools.headers import headers_header
from tools.base64_text import text_conversion_base64
from tools.handl_specialcharacters import hzs_sub
from tools.response_api import response_api


def community_data_capture():
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    nowTime = (datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S")
    nowTime_hd = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
    url = "https://mobile-gate.611.com/api/CirlcleData"
    t = 24
    for i in range(24):
        minTime = (datetime.datetime.now() + datetime.timedelta(hours=-t)).strftime("%Y-%m-%d %H:%M:%S")
        t = t - 1
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
        # print("--", rep)
        data_list_count = int(len(rep["data"]["list"]))
        for j in range(data_list_count):
            community_info = {}
            title = str(rep["data"]["list"][j]["displayDatas"][0]["title"])
            subhead = str(rep["data"]["list"][j]["displayDatas"][0]["contentTxt"])
            if subhead.find("肺炎") != -1 or subhead.find("新冠") != -1:
                print("subhead:", subhead)
                print("非法字符放弃！")
                continue
            # 发布者者昵称
            nickName = str(rep["data"]["list"][j]["displayDatas"][0]["user"]["nickName"])
            headImageUrl = str(rep["data"]["list"][j]["displayDatas"][0]["user"]["headImageUrl"])
            contentId = str(rep["data"]["list"][j]["displayDatas"][0]["contentId"])
            # # 点赞数
            # hitsCount = str(rep["data"]["list"][i]["displayDatas"][0]["hitsCount"])
            # 发布时间
            pubTime = str(rep["data"]["list"][j]["displayDatas"][0]["pubTime"])
            # "pubTimeStr": "1小时前",		"srcName": "我为鞋狂圈", "contentTxt": " mediaList: littleImg
            pubTimeStr = str(rep["data"]["list"][j]["displayDatas"][0]["pubTimeStr"])
            # 标签
            contentTxt = str(rep["data"]["list"][j]["displayDatas"][0]["contentTxt"])
            srcName = str(rep["data"]["list"][j]["displayDatas"][0]["srcName"])
            mediaList_count = int(len(rep["data"]["list"][j]["displayDatas"][0]["mediaList"]))
            if mediaList_count == 0:
                print("mediaList_count 为零 放弃")
                continue
            littleImg = str(rep["data"]["list"][j]["displayDatas"][0]["mediaList"][0]["littleImg"])
            # print(title, contentId, hitsCount, pubTime, pubTimeStr, srcName, contentTxt, littleImg)
            if int(len(contentTxt)) > 50:
                if int(len(littleImg)) > 0:
                    url_info = "https://mobile-gate.611.com/api/DetailDataInfo"
                    data_info = {"infoId": contentId, "publishDate": pubTime}
                    html_result = requests.post(url=url_info, data=data_info, headers=headers).text
                    # print(html_result)
                    html_result = json.loads(html_result)
                    contentTxt = ""
                    # contentTxt
                    htmlContent = str(html_result["data"]["headList"]["htmlContent"]).replace("\n", "")
                    contentTxt_count = int(len(html_result["data"]["contentDatas"]))
                    icon_image = ""
                    for cont_count in range(contentTxt_count):
                        if "content" in html_result["data"]["contentDatas"][cont_count]:
                            content = str(html_result["data"]["contentDatas"][cont_count]["content"])
                            contentTxt = contentTxt + "<p>" + content + "</p></br>"
                        else:
                            content = html_result["data"]["contentDatas"][cont_count].setdefault("content", "")
                        if "icon" in html_result["data"]["contentDatas"][cont_count]:
                            icon_image = str(html_result["data"]["contentDatas"][cont_count]["icon"])

                    community_info["title"] = title.replace("乐鱼体育", "").replace("彩经", "")
                    community_info["subhead"] = subhead
                    community_info["nickName"] = nickName
                    community_info["HeadImgUrl"] = headImageUrl
                    community_info["channelIconPath"] = ""
                    community_info["contentId"] = contentId
                    community_info["hitsCount"] = str(random.randint(100, 2000))
                    community_info["pubTime"] = pubTime
                    community_info["pubTimeStr"] = pubTimeStr
                    community_info["srcName"] = srcName
                    community_info["littleImg"] = littleImg
                    contentTxt = contentTxt.replace("乐鱼体育", "").replace("彩经", "")
                    community_info["contentTxt"] = contentTxt
                    # print("htmlContent", htmlContent)
                    community_info["htmlContent"] = text_conversion_base64(htmlContent)
                    community_info["icon_image"] = icon_image
                    commun_url = "https://mobile-gate.611.com/api/DetailDataComnments"
                    commun_data = {"infoId": contentId, "publishDate": pubTime, "isHot": "false", "minTime": ""}
                    commun_info = json.loads(requests.post(url=commun_url, data=commun_data, headers=headers).text)
                    comment_list = []
                    data_count = 0
                    if "data" in commun_info:
                        data_count = len(commun_info["data"])
                    else:
                        commun_info.setdefault("data", "")
                    if data_count > 0:
                        print("评论", data_count)
                    for d_count in range(int(len(commun_info["data"]))):
                        comment_dict = {}
                        id = commun_info["data"][d_count]["id"]
                        userId = commun_info["data"][d_count]["user"]["userId"]
                        headImageUrl = commun_info["data"][d_count]["user"]["headImageUrl"]
                        nickName = commun_info["data"][d_count]["user"]["nickName"]
                        nickName = hzs_sub(nickName)
                        postdate = commun_info["data"][d_count]["postdate"]
                        content = commun_info["data"][d_count]["content"]
                        content = text_conversion_base64(content)
                        comment_dict["id"] = id
                        comment_dict["userId"] = userId
                        comment_dict["headImageUrl"] = headImageUrl
                        comment_dict["nickName"] = nickName
                        comment_dict["postdate"] = postdate
                        comment_dict["content"] = content
                        comment_list.append(comment_dict)
                    community_info["comment"] = comment_list

                    print("当前时间：", nowTime_hd, ":发布时间", pubTime)
                    url_tj = "/community/save_community"
                    response_api(url_tj, community_info)


if __name__ == '__main__':
    community_data_capture()
