import sys
sys.path.append("/opt/data_captureAPP")
import requests
import json
import random
import datetime
import pymysql
import base64
from tools.headers import headers_header

def community_data_capture():
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    nowTime = (datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S")
    # print(nowTime, minTime)
    url = "https://mobile-gate.611.com/api/CirlcleData"
    t = 24
    for i in range(24):
        minTime = (datetime.datetime.now() + datetime.timedelta(hours=-t)).strftime("%Y-%m-%d %H:%M:%S")
        t = t - 1
        data = {
            "minTime": str(minTime),
            "customValue": "",
            "maxTime": str(nowTime)}

        # lytime: 2020 - 10 - 21 10: 27:22
        headers = {
            "deviceid": deviceid,
            "deviceaid": deviceaid,
            "requestRam": requestRam,
            "sign": sign,
            "lytime": lytime,
            "source": source
        }
        # print(url)
        # print(headers)
        # print(data)
        rep = requests.post(url=url, data=data, headers=headers)
        rep = json.loads(rep.text)
        # print(rep)
        for j in range(int(len(rep["data"]["list"]))):
            community_info = {}
            title = str(rep["data"]["list"][j]["displayDatas"][0]["title"])
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
            srcName = str(rep["data"]["list"][j]["displayDatas"][0]["srcName"])
            contentTxt = str(rep["data"]["list"][j]["displayDatas"][0]["contentTxt"])
            littleImg = str(rep["data"]["list"][j]["displayDatas"][0]["mediaList"][0]["littleImg"])
            # print(title, contentId, hitsCount, pubTime, pubTimeStr, srcName, contentTxt, littleImg)
            if int(len(contentTxt)) > 50:
                if int(len(littleImg)) > 0:
                    title = title.replace("乐鱼体育", "").replace("彩经", "")
                    community_info["title"] = title
                    community_info["nickName"] = nickName
                    community_info["HeadImgUrl"] = headImageUrl
                    channelIconPath = ""
                    community_info["channelIconPath"] = channelIconPath
                    community_info["contentId"] = contentId
                    hitsCount = str(random.randint(100, 2000))
                    community_info["hitsCount"] = hitsCount
                    community_info["pubTime"] = pubTime
                    community_info["pubTimeStr"] = pubTimeStr
                    community_info["srcName"] = srcName
                    contentTxt = contentTxt.replace("乐鱼体育", "").replace("彩经", "")
                    community_info["contentTxt"] = contentTxt
                    community_info["littleImg"] = littleImg
                    # print(nowTime_hd, ":", community_info)

                    comment_url = "https://mobile-gate.611.com/api/DetailDataComnments"
                    comment_data = {"infoId": contentId, "publishDate": pubTime, "isHot": "false",
                                    "minTime": ""}
                    comment_headers = {
                        "deviceid": "1217bd0c9497d7c624aee3d2b2ad13a6",
                        "deviceaid": "1217bd0c9497d7c624aee3d2b2ad13a6",
                        "requestRam": "1604890356",
                        "sign": "d9051b8dd6e1687b847e0ea0b208381e",
                        "lytime": "2020-11-09 10:52:36",
                        "source": "1"
                    }
                    comment_result = requests.post(url=comment_url, data=comment_data, headers=comment_headers).text
                    comment_result = json.loads(comment_result)
                    # print("comment_result-----:", comment_result)
                    if "data" in comment_result:
                        data = len(comment_result["data"])
                    else:
                        comment_result.setdefault("data", "")
                    try:
                        db = pymysql.connect("47.97.79.60", "root", "#2020mysql56root", "tyds", charset='utf8')
                        # 使用cursor()方法获取操作游标
                        cursor = db.cursor()
                        sql_query = "SELECT * FROM communities  WHERE contentId='%s' " % (contentId)
                        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime(
                            "%Y-%m-%d %H:%M:%S")
                        cursor.execute(sql_query)
                        data_query = cursor.rowcount
                        if data_query == 0:
                            id_query = "SELECT MAX(id) FROM communities "
                            num = cursor.execute(id_query)
                            if num > 0:
                                num1 = cursor.fetchall()
                                ids = num1[0]
                                id = ids[0]
                                if id == None:
                                    id = 1
                                else:
                                    id = id + 1

                            print("-------------社区ID" + contentId + "插入成功：时间" + capture_time + "-----------------")
                            # # SQL 插入语句
                            sql_insert = "INSERT INTO communities (contentId,title,nickName, hitsCount, pubTime, srcName," \
                                         "contentTxt,littleImg,id,channelIconPath,HeadImgUrl)" \
                                         "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%d','%s','%s')" \
                                         % (
                                             contentId, title, nickName, hitsCount, pubTime, srcName, contentTxt,
                                             littleImg, id, channelIconPath, headImageUrl)

                            # 执行sql语句
                            cursor.execute(sql_insert)
                        else:
                            print(contentId, "社区已存在,不能插入数据-------")
                            continue

                        # 提交到数据库执行

                        comment_list = []
                        for community_count in range(int(len(comment_result["data"]))):
                            comment_dict = {}
                            # print(comment_result["data"][community_count])
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
                            content1 = base64.b64encode(content.encode('utf-8'))
                            content2 = (str(content1, 'utf-8'))
                            comment_dict["content"] = content2

                            comment_list.append(comment_dict)
                        comment_list = str(comment_list).replace("'", '"')
                        print("comment_list:", comment_list)
                        print("-------------评论" + contentId + "-----------------")
                        # SQL 插入语句
                        sql_insert = "INSERT INTO comment(contentId,communities_json) VALUES ('%s','%s')" % (
                            contentId, comment_list)
                        # 执行sql语句
                        cursor.execute(sql_insert)
                        # 提交到数据库执行
                        db.commit()
                    except Exception as e:
                        print(
                            "————————————————————————————插入数据异常,事物已回滚" + capture_time + "————————————————————————————————————")
                        db.rollback()
                        print(e)

                    # 关闭数据库连接
                    db.close()
            print("组装成功的json数据", str(community_info).replace("'", '"'))
            print("")


if __name__ == '__main__':
    community_data_capture()
