import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from tools.random_number import *
from tools.time_treatment import *
from tools.base64_text import text_conversion_base64
from tools.handl_specialcharacters import hzs_sub
from tools.random_number import random_circle_list
from tools.response_api import response_api


def community_data_capture():
    url_communt = "https://shequ.sports.qq.com/topic/homePageByType?&personalSwitchClose=0&os=android&osvid=23&osVersion=6.0.1&appvid=6.4.00.932&appvcode=932&network=wifi&store=96&width=720&height=1280&guid=2d9ecb0c76397e563577a752100017f14b17&qimei=2d9ecb0c76397e563577a752100017f14b17&androidId=1e1080316fa234be&xgToken=0319bc3c2c62538a99fb7b5f6e41a2a2b630&deviceId=500000000254941&cpuArch=x86&timezone=Asia%2FShanghai&pixelRatio=1.5&manufacturer=HUAWEI&deviceModel=ALP-AL00"
    headers_communt = {"Content-Type": "application/x-www-form-urlencoded"}
    data = "columnId=hot&times=1&flag=0"
    communt = requests.post(url=url_communt, data=data, headers=headers_communt).text
    communt = json.loads(communt)
    communt_count = int(len(communt["data"]["list"]))
    for com_count in range(communt_count):
        base = {}
        title = communt["data"]["list"][com_count]["info"]["title"]
        subhead = str(communt["data"]["list"][com_count]["info"]["summary"]).replace("\xa0", "").replace("#", "")
        if subhead.find("肺炎") != -1 or subhead.find("新冠") != -1:
            print("subhead:", subhead)
            print("非法字符放弃！")
            continue
        title = hzs_sub(title)
        if int(len(title)) < 5:
            print(title, "title长度小于5放弃")
            print("")
            continue
        images_count = int(len(communt["data"]["list"][com_count]["info"]["images"]))
        if images_count > 0:
            littleImg = communt["data"]["list"][com_count]["info"]["images"][0]
        else:
            littleImg = ""
        nickName = str(communt["data"]["list"][com_count]["info"]["user"]["name"]).replace("'", " ")
        headImageUrl = communt["data"]["list"][com_count]["info"]["user"]["avatar"]
        channelIconPath = communt["data"]["list"][com_count]["info"]["moduleIcon"]
        imageDatas_count = int(len(communt["data"]["list"][com_count]["info"]["imageDatas"]))
        if imageDatas_count > 0:
            icon_image = communt["data"]["list"][com_count]["info"]["imageDatas"][0]["cur"]["url"]
        else:
            continue
        contentId = communt["data"]["list"][com_count]["id"]
        hitsCount = random_number_likes()
        pubTime = now_time_revert(10)
        pubTimeStr = "两小时前"
        srcName = random_circle_list()
        come_from = "腾讯体育"
        capture_time = now_time()
        capture_type = "社区"
        url_info = "https://shequ.sports.qq.com/topic/detail?tid=" + str(
            contentId) + "&showSupporter=1&needRecmd=1&showHolder=true&personalSwitchClose=0&os=android&osvid=23&osVersion=6.0.1&appvid=6.4.00.932&appvcode=932&network=wifi&store=96&width=720&height=1280&guid=2d9ecb0c76397e563577a752100017f14b17&qimei=2d9ecb0c76397e563577a752100017f14b17&androidId=1e1080316fa234be&xgToken=0319bc3c2c62538a99fb7b5f6e41a2a2b630&deviceId=500000000254941&cpuArch=x86&timezone=Asia%2FShanghai&pixelRatio=1.5&manufacturer=HUAWEI&deviceModel=ALP-AL00"
        communt_info = requests.get(url=url_info).text
        communt_info = json.loads(communt_info)
        # print(communt_info)
        content_count = int(len(communt_info["data"]["topic"]["content"]))
        contentTxt = ""
        htmlContent = ""
        for con_count in range(content_count):
            content = communt_info["data"]["topic"]["content"][con_count]["info"]
            if content != "":
                if content.find("http") == -1:
                    if int(len(subhead)) == 0:
                        subhead = str(content).replace("\xa0", "").replace("#", "")
                    contentTxt = contentTxt + "<p>" + content + "</p></br>"
                    htmlContent = htmlContent + "<p>" + content + "</p></br>"
                else:
                    htmlContent = htmlContent + "<p><img src =" + content + " ></p></br>"
        base["title"] = title
        if int(len(subhead)) < 5:
            print(title, "subhead长度小于5放弃")
            print("")
            continue

        base["subhead"] = subhead
        base["littleImg"] = littleImg
        nickName = hzs_sub(nickName)
        if nickName == "":
            nickName = random_circle_list()
        base["nickName"] = nickName
        base["HeadImgUrl"] = headImageUrl
        base["channelIconPath"] = channelIconPath
        base["contentId"] = contentId
        base["hitsCount"] = hitsCount
        base["pubTime"] = pubTime
        base["pubTimeStr"] = pubTimeStr
        base["srcName"] = srcName
        base["icon_image"] = icon_image
        base["contentTxt"] = contentTxt
        # print("htmlContent", htmlContent)
        base["htmlContent"] = text_conversion_base64(htmlContent)
        base["come_from"] = come_from
        base["capture_time"] = capture_time
        base["capture_type"] = capture_type

        url_coms = "https://shequ.sports.qq.com/reply/listByTypeV2?tid=" + str(
            contentId) + "&lastId=0&listType=hot&sort=acs&showType=all&included=0&personalSwitchClose=0&os=android&osvid=23&osVersion=6.0.1&appvid=6.4.00.932&appvcode=932&network=wifi&store=96&width=720&height=1280&guid=2d9ecb0c76397e563577a752100017f14b17&qimei=2d9ecb0c76397e563577a752100017f14b17&androidId=1e1080316fa234be&xgToken=0319bc3c2c62538a99fb7b5f6e41a2a2b630&deviceId=500000000254941&cpuArch=x86&timezone=Asia%2FShanghai&pixelRatio=1.5&manufacturer=HUAWEI&deviceModel=ALP-AL00"
        coms = requests.get(url=url_coms).text
        coms = json.loads(coms)
        coms_list_count = int(len(coms["data"]["list"]))
        if coms_list_count > 0:
            print("评论：", coms_list_count)
        coms_list = []
        for com_count in range(coms_list_count):
            coms_dict = {}
            id = coms["data"]["list"][com_count]["id"]
            userid = coms["data"]["list"][com_count]["user"]["id"]
            headImageUrl = coms["data"]["list"][com_count]["user"]["avatar"]
            nickName = str(coms["data"]["list"][com_count]["user"]["name"]).replace("'", " ")
            postdate = coms["data"]["list"][com_count]["createTime"]
            postdate = timestamp_conversion_date(postdate)
            content = coms["data"]["list"][com_count]["content"][0]["info"]

            coms_dict["id"] = id
            coms_dict["userid"] = userid
            coms_dict["headImageUrl"] = headImageUrl
            nickName = hzs_sub(nickName)
            if nickName == "":
                nickName = random_circle_list()
            coms_dict["nickName"] = nickName
            coms_dict["postdate"] = postdate
            coms_dict["content"] = text_conversion_base64(content)
            coms_list.append(coms_dict)
        base["comment"] = coms_list
        url_tj = "/community/save_community"
        response_api(url_tj, base)


if __name__ == '__main__':
    community_data_capture()
