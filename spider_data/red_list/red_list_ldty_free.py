import sys

sys.path.append("/opt/data_captureAPP")
import json
import requests
import time
import datetime
import base64
import random
from tools.response_api import response_api


# 免费红单
def red_list_fkhd():
    url = "https://api.liaodaotiyu.com/custom/projTypeList.do?pageNum=1&gameid=70&pageSize=100&free=0&mobileType=1&loginType=1&appVersion=1.8.3&source=1005&imei=890d4da3eb9d66f01e9cfd7164779ab5&userType=1"
    headers = {"Host": "api.liaodaotiyu.com"
               }
    result_list = requests.get(url=url, headers=headers)
    result_list = json.loads(result_list.text)
    result_list_count = int(len(result_list["data"]["list"]))
    count_redlist = 1
    for r_count in range(result_list_count):
        print("共有红单数据", result_list_count, "条，正在处理第", count_redlist, "条数据")
        count_redlist = count_redlist + 1
        base = {}
        if "photo" in result_list["data"]["list"][r_count]:
            photo = result_list["data"]["list"][r_count]["photo"]
        else:
            photo = result_list["data"]["list"][r_count].setdefault("photo", "")

        title = str(result_list["data"]["list"][r_count]["title"]).replace("\n", "").replace("\n", "")
        userid = result_list["data"]["list"][r_count]["userid"]
        nickName = result_list["data"]["list"][r_count]["nickid"]
        projid = result_list["data"]["list"][r_count]["projid"]
        matchtime = result_list["data"]["list"][r_count]["matchtime"]
        matchtime = str(matchtime)[0:10]
        matchtime = int(matchtime)
        matchtime = time.localtime(matchtime)
        matchtime = time.strftime("%Y-%m-%d %H:%M:%S", matchtime)
        match = {}
        m = json.loads(result_list["data"]["list"][r_count]["match"])
        leagueName = m["leagueName"]
        itemid = m["itemid"]
        hn = m["hn"]
        gn = m["gn"]
        m["matchtime"] = matchtime
        name = m["name"]
        match["leagueName"] = leagueName
        match["itemid"] = itemid
        match["hn"] = hn
        match["gn"] = gn
        match["mt"] = m["matchtime"]
        match["name"] = name
        base["match"] = match

        gameid = result_list["data"]["list"][r_count]["gameid"]
        price = result_list["data"]["list"][r_count]["price"]
        # 近 lastpub 中 lasthit
        lastpub = result_list["data"]["list"][r_count]["lastpub"]
        lasthit = result_list["data"]["list"][r_count]["lasthit"]
        # label 标签

        if "label" in result_list["data"]["list"][r_count]:
            label = result_list["data"]["list"][r_count]["label"]
        else:
            label = result_list["data"]["list"][r_count].setdefault("label", "")
        hotValue = result_list["data"]["list"][r_count]["hotValue"]

        base["photo"] = photo
        base["title"] = title
        base["userid"] = userid
        base["nickName"] = nickName
        base["projid"] = projid
        base["matchtime"] = matchtime
        base["match"] = match
        base["gameid"] = gameid
        base["price"] = random.randint(10, 50)
        base["lastpub"] = lastpub
        base["lasthit"] = lasthit
        base["label"] = label
        base["hotValue"] = hotValue
        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
        base["come_from"] = "料到"
        base["capture_time"] = capture_time
        base["capture_type"] = "红单"
        print(title)
        # https://api.liaodaotiyu.com/custom/projinfolook.do?projid=702020111923060463757&mobileType=1&loginType=1&appVersion=1.8.3&source=1005&imei=890d4da3eb9d66f01e9cfd7164779ab5&userType=1
        info_url = "https://api.liaodaotiyu.com/custom/projinfolook.do?projid=" + str(
            projid) + "&mobileType=1&loginType=1&appVersion=1.8.3&source=1005&imei=890d4da3eb9d66f01e9cfd7164779ab5&userType=1"
        info_headers = {"Host": "api.liaodaotiyu.com",
                        "appid": "C_ZIH2G0Y2HF01120G09AX2SA94K7F647",
                        "accessToken": "+NEflO3uj02MBMS5Y1lDrc6rfw3xAyaU8ZlKclK4SvlPzRiDlKrv6y3zJGtffvBdKF6AYVnNxGvS3wlhmESOQzvnV0+m8vTnZpAO6nw0+A/5hWj7vOhi+96WwAeqFk4U8BlC0rNTxYsHisUaz+J0iJnaIcB77AkU15uzN1qR114="
                        }
        info_single = requests.post(url=info_url, headers=info_headers)
        # print(info_single.text)
        info_single = json.loads(info_single.text)
        pubDate = info_single["data"]["pubDate"]
        if "content" in info_single["data"]:
            content = info_single["data"]["content"]
            print("content:", content)
            if int(len(content)) == 0:
                print("推荐理由_内容为:", int(len(content)), ",放弃!")
                print("")
                continue
            content1 = base64.b64encode(content.encode('utf-8'))
            content2 = (str(content1, 'utf-8'))
            base["content"] = content2
        else:
            content = info_single["data"].setdefault("content", "")
            print("推荐理由_内容为:", int(len(content)), ",放弃!")
            print("")
            continue

        pubDate = str(pubDate)[0:10]
        pubDate = int(pubDate)
        pubDate = time.localtime(pubDate)
        pubDate = time.strftime("%Y-%m-%d %H:%M:%S", pubDate)
        base["pubDate"] = pubDate
        matcharray_count = int(len(info_single["data"]["matcharray"]))
        matcharray_list = []
        for m_count in range(matcharray_count):
            matcharray_dict = {}
            hid = info_single["data"]["matcharray"][m_count]["hid"]
            gid = info_single["data"]["matcharray"][m_count]["gid"]
            hn = info_single["data"]["matcharray"][m_count]["hn"]
            gn = info_single["data"]["matcharray"][m_count]["gn"]
            mt = matchtime
            spf = info_single["data"]["matcharray"][m_count]["spf"]
            leagueName = info_single["data"]["matcharray"][m_count]["leagueName"]
            rqspf = info_single["data"]["matcharray"][m_count]["rqspf"]
            name = info_single["data"]["matcharray"][m_count]["name"]
            state = info_single["data"]["matcharray"][m_count]["state"]
            matcharray_dict["hid"] = hid
            matcharray_dict["gid"] = gid
            matcharray_dict["hn"] = hn
            matcharray_dict["gn"] = gn
            matcharray_dict["mt"] = mt
            matcharray_dict["spf"] = spf
            matcharray_dict["leagueName"] = leagueName
            matcharray_dict["rqspf"] = rqspf
            matcharray_dict["name"] = name
            matcharray_dict["state"] = state
            matcharray_list.append(matcharray_dict)
        base["matcharray"] = matcharray_list
        share = {}
        shareUrl = info_single["data"]["share"]["shareUrl"]
        share_title = info_single["data"]["share"]["title"]
        subTitle = info_single["data"]["share"]["subTitle"]
        share["shareUrl"] = shareUrl
        share["title"] = share_title
        share["subTitle"] = subTitle
        base["share"] = share
        url_redlist = "/hongdan/save_hongdan"
        response_api(url_redlist, base)


if __name__ == '__main__':
    red_list_fkhd()
