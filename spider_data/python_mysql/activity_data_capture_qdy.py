import sys

sys.path.append("/opt/data_captureAPP")
import json
import requests
import time
import datetime
import pymysql
import random
from tools.handl_specialcharacters import hzs_sub


def activity_data_capture_qdy():
    try:
        # /opt/data_captureAPP/python_mysql/
        # activity_no_data = "/opt/data_captureAPP/python_mysql/activity_no_data.txt"
        activity_no_data = "activity_no_data.txt"

        with open(activity_no_data, "r", encoding="utf-8") as fpage:
            page = int(fpage.read())
            print("page", page)
            for p in range(500):
                base = {}
                url = "https://m.quyundong.com/Forum/index/getDetial?huodong_id=" + str(page)
                activity_json = requests.get(url=url)
                activity_json = json.loads(activity_json.text)
                # {"status":4401,"msg":"\u6d3b\u52a8\u4e0d\u5b58\u5728","data":[]}
                if activity_json["status"] != '0000':
                    print("无活动数据：" + str(page))
                    with open(activity_no_data, "w", encoding="utf-8")as f:
                        f.write(str(page + 1))
                    break
                page = page + 1

                with open(activity_no_data, "w", encoding="utf-8")as f:
                    f.write(str(page))
                # print(activity_json)

                huodong_id = activity_json["data"]["huodong_id"]
                base["huodong_id"] = huodong_id
                cat_id = activity_json["data"]["cat_id"]
                base["cat_id"] = cat_id
                venues_id = activity_json["data"]["venues_id"]
                base["venues_id"] = venues_id
                start_time = activity_json["data"]["start_time"]
                start_time = time.localtime(int(start_time))
                start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_time)
                base["start_time"] = start_time

                end_time = activity_json["data"]["end_time"]
                end_time = time.localtime(int(end_time))
                end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_time)
                base["end_time"] = end_time

                deadline = activity_json["data"]["deadline"]
                deadline = time.localtime(int(deadline))
                deadline = time.strftime("%Y-%m-%d %H:%M:%S", deadline)
                base["deadline"] = deadline
                price = activity_json["data"]["price"]
                base["price"] = price
                address = activity_json["data"]["address"]
                base["address"] = address
                longitude = activity_json["data"]["longitude"]
                base["longitude"] = longitude
                latitude = activity_json["data"]["latitude"]
                base["latitude"] = latitude
                user_id = activity_json["data"]["user_id"]
                base["user_id"] = user_id
                user_name = activity_json["data"]["user_name"]
                base["user_name"] = user_name
                phone = activity_json["data"]["phone"]
                base["phone"] = phone
                avatar = activity_json["data"]["avatar"]
                base["avatar"] = avatar
                content = hzs_sub(activity_json["data"]["content"])
                print(content)
                base["content"] = hzs_sub(content)
                club_id = activity_json["data"]["club_id"]
                base["club_id"] = club_id
                club_name = activity_json["data"]["club_name"]
                base["club_name"] = club_name
                title = activity_json["data"]["share_info"]["title"]
                base["title"] = title
                content_time = str(activity_json["data"]["share_info"]["content"]).replace("\n", "</br>")
                base["content_time"] = content_time
                cat_name = activity_json["data"]["cat_name"]
                base["cat_name"] = cat_name
                icon_url = activity_json["data"]["icon_url"]
                base["icon_url"] = icon_url
                status = activity_json["data"]["status"]
                ext_pingfen = random.randint(1, 5)
                if int(len(club_name)) > 0:
                    if int(len(content)) > 0:
                        status_if = int(status)
                        if status_if == 2:
                            base["status"] = "已开始"
                            base["status_code"] = 1
                            status_code = 1
                            status = "已开始"
                        else:
                            base["status"] = "待开始"
                            base["status_code"] = 0
                            status_code = 0
                            status = "待开始"
                        come_from = "趣运动"
                        base["come_from"] = come_from
                        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
                        base["capture_time"] = capture_time
                        capture_type = "活动"
                        base["capture_type"] = capture_type
                        h_count1 = random.randint(12, 50)
                        if h_count1 > 12:
                            h_count2 = random.randint(3, 9)
                            h_count3 = h_count1 - h_count2
                            count_person = str(str(h_count3) + "/" + str(h_count1))
                            # print(type(count_person))
                            # print(count_person)

                        db = pymysql.connect("47.97.79.60", "root", "#2020mysql56root", "tyds", charset='utf8')
                        # 使用cursor()方法获取操作游标
                        cursor = db.cursor()
                        try:
                            sql_query = "SELECT * FROM activities  WHERE huodong_id='%s' " % (huodong_id)
                            cursor.execute(sql_query)
                            data_query = cursor.rowcount
                            if data_query == 0:
                                json_base = str(base).replace("'", '"')
                                print("-------------活动ID " + huodong_id + "：时间" + capture_time + "-----------------")
                                # # SQL 插入语句
                                sql_insert = "INSERT INTO activities (huodong_id,cat_id,cat_name,venues_id, start_time, end_time, deadline," \
                                             "price,address,longitude,latitude,user_id,user_name,phone,avatar,content,club_id,club_name," \
                                             "icon_url,status_code,status,title,count_person,content_time,come_from,capture_time,capture_type,json,ext_pingfen) " \
                                             "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                                             "'%s','%s','%s','%s','%s','%d','%s','%s','%s','%s','%s','%s','%s','%s','%d')" % (
                                                 huodong_id, cat_id, cat_name, venues_id,
                                                 start_time, end_time, deadline,
                                                 price, address, longitude,
                                                 latitude, user_id, user_name,
                                                 phone, avatar, content, club_id,
                                                 club_name, icon_url, status_code, status,
                                                 title, count_person, content_time, come_from,
                                                 capture_time, capture_type, json_base, ext_pingfen)
                                cursor.execute(sql_insert)
                            else:
                                print(huodong_id, capture_time, "活动数据已存在,不能插入数据库-----------")
                                continue

                            user_list = []
                            # print("user_list", len(activity_json["data"]["user_list"]))
                            if int(len(activity_json["data"]["user_list"])) > 0:
                                for i in range(int(len(activity_json["data"]["user_list"]))):
                                    user_dict = {}
                                    user_id = activity_json["data"]["user_list"][i]["user_id"]
                                    avatar = activity_json["data"]["user_list"][i]["avatar"]
                                    user_name = activity_json["data"]["user_list"][i]["user_name"]
                                    user_dict["user_id"] = user_id
                                    user_dict["avatar"] = avatar
                                    user_dict["user_name"] = user_name
                                    user_list.append(user_dict)
                                base["user_list"] = user_list
                                user_list = str(user_list).replace("'", '"')
                                sql_insert = "INSERT INTO activites_user_list (rid,json)" \
                                             "VALUES ('%s','%s')" \
                                             % (huodong_id, user_list)
                                # print("sql_insert",sql_insert)
                                cursor.execute(sql_insert)

                            tags_list = []
                            # print("tags", len(activity_json["data"]["tags"]))
                            if int(len(activity_json["data"]["tags"])) > 0:
                                for j in range(int(len(activity_json["data"]["tags"]))):
                                    tags_dict = {}
                                    tag_id = activity_json["data"]["tags"][j]["tag_id"]
                                    name = activity_json["data"]["tags"][j]["name"]
                                    color = activity_json["data"]["tags"][j]["color"]
                                    tags_dict["tag_id"] = tag_id
                                    tags_dict["name"] = name
                                    tags_dict["color"] = color
                                    tags_list.append(tags_dict)
                                base["tags"] = tags_list
                                tags_list1 = str(tags_list).replace("'", '"')
                                sql_insert = "INSERT INTO activites_tags (rid,json)" \
                                             "VALUES ('%s','%s')" \
                                             % (huodong_id, tags_list1)
                                # print("sql_insert",sql_insert)
                                cursor.execute(sql_insert)

                            db.commit()
                        except Exception as e:
                            print(
                                "————————————————————————————插入数据失败,事物已回滚" + capture_time + "————————————————————————————————————")
                            activity_data_capture_qdy()
                            db.rollback()
                            print(e)
                        db.close()

                        print("组装成功的json数据", str(base).replace("'", '"'))
                        print("")
    except Exception as e1:
        s_time = 30
        print("出现错误", s_time, "秒再次执行")
        time.sleep(s_time)
        print(e1)
        print("")
        activity_data_capture_qdy()


if __name__ == '__main__':
    activity_data_capture_qdy()
