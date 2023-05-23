import sys

sys.path.append("/opt/data_captureAPP")
import json
import requests
import time
import base64
from tools.response_api import *


# 转会市场
def capture_bmb_transfermarket():
    now = str(int(time.time()))
    transfermarket_url = "http://api.snsports.cn/api/content/phone/GetBMMarketList.json?&cityId=5643&sportType=%E8%B6%B3%E7%90%83&pageSize=100&pageNum=1&type=bm_team&passport=ijhe6ombkdk4ln5rqhuicbc8zcer3or6&appVersion=3.5.1&device=androidphone&timestamp=" + now + "892&sign=acf8d754d34de80cd70d808d219f6a4a786a0b09&apikey=7f4880f7ab5dd50d53"
    transfermarket = requests.get(url=transfermarket_url)
    transfermarket = json.loads(transfermarket.text)
    transfermarket_count = int(len(transfermarket["messages"]["data"]["bmMarketList"]))
    for tf_count in range(transfermarket_count):
        base = {}
        title = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["title"]
        # base 64
        summary = str(transfermarket["messages"]["data"]["bmMarketList"][tf_count]["summary"]).replace("\n", "</br>")
        summary = base64.b64encode(summary.encode('utf-8'))
        summary = (str(summary, 'utf-8'))
        needStrengthenPosition = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["needStrengthenPosition"]
        favorArea = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["favorArea"]
        createDate = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["createDate"]
        createDate = str(createDate).replace("T", " ").split("+")[0]
        id = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["id"]

        base["title"] = title
        base["summary"] = summary
        base["needStrengthenPosition"] = needStrengthenPosition
        base["favorArea"] = favorArea
        base["createDate"] = createDate
        base["id"] = id
        sportType = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["userInfo"]["sportType"]
        base["sportType"] = sportType

        badge = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["teamInfo"]["badge"]
        if badge.find("http") == -1:
            badge = "http://images.snsports.cn/" + badge
        name = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["teamInfo"]["name"]

        teamInfo = {}
        teamInfo["name"] = name
        teamInfo["badge"] = badge
        base["teamInfo"] = teamInfo

        userInfo = {}
        nickName = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["userInfo"]["nickName"]
        profile = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["userInfo"]["profile"]
        if profile.find("http") == -1:
            profile = "http://images.snsports.cn/" + profile
        user_id = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["userInfo"]["id"]

        userInfo["nickName"] = nickName
        userInfo["profile"] = profile
        userInfo["user_id"] = user_id

        base["userInfo"] = userInfo

        image_count = int(len(transfermarket["messages"]["data"]["bmMarketList"][tf_count]["image"]))
        image_list = []
        for i_count in range(image_count):
            image_dict = {}
            width = str(transfermarket["messages"]["data"]["bmMarketList"][tf_count]["image"][i_count]["width"])
            height = str(transfermarket["messages"]["data"]["bmMarketList"][tf_count]["image"][i_count]["height"])
            img_url = transfermarket["messages"]["data"]["bmMarketList"][tf_count]["image"][i_count]["url"]
            if img_url.find("http") == -1:
                img_url = "http://images.snsports.cn/" + img_url
            image_dict["width"] = width
            image_dict["height"] = height
            image_dict["img_url"] = img_url
            image_list.append(image_dict)
        base["image"] = image_list

        url_transfermarket = "/hotmatch/save_transfermarket"
        response_api(url_transfermarket, base)


if __name__ == '__main__':
    capture_bmb_transfermarket()
