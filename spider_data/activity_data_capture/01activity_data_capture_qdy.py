import sys
sys.path.append("/opt/data_captureAPP")
import json
import requests
from tools.time_treatment import *


def activity_data_capture_qdy():
    hd_count = 45000
    for k in range(5000):
        hd_count = hd_count + 1
        base = {}
        url = "https://m.quyundong.com/Forum/index/getDetial?huodong_id=" + str(hd_count)
        activity_json = requests.get(url=url)
        activity_json = json.loads(activity_json.text)
        if activity_json["status"] != '0000':
            print("无活动数据" + str(hd_count))
            continue
        # print(activity_json)
        base["huodong_id"] = activity_json["data"]["huodong_id"]
        base["cat_id"] = activity_json["data"]["cat_id"]
        base["venues_id"] = activity_json["data"]["venues_id"]
        start_time = activity_json["data"]["start_time"]
        base["start_time"] = timestamp_conversion_date(start_time)

        end_time = activity_json["data"]["end_time"]
        base["end_time"] = timestamp_conversion_date(end_time)

        deadline = activity_json["data"]["deadline"]
        base["deadline"] = timestamp_conversion_date(deadline)
        base["price"] = activity_json["data"]["price"]
        base["address"] = activity_json["data"]["address"]
        base["longitude"] = activity_json["data"]["longitude"]
        base["latitude"] = activity_json["data"]["latitude"]
        base["user_id"] = activity_json["data"]["user_id"]
        base["user_name"] = activity_json["data"]["user_name"]
        base["phone"] = activity_json["data"]["phone"]
        base["avatar"] = activity_json["data"]["avatar"]
        base["content"] = activity_json["data"]["content"]
        base["club_id"] = activity_json["data"]["club_id"]
        base["club_name"] = activity_json["data"]["club_name"]
        base["title"] = activity_json["data"]["share_info"]["title"]
        base["content_time"] = str(activity_json["data"]["share_info"]["content"]).replace("\n", "</br>")
        base["cat_name"] = activity_json["data"]["cat_name"]
        base["icon_url"] = activity_json["data"]["icon_url"]
        base["come_from"] = "趣运动"
        base["capture_time"] = now_time()
        base["capture_type"] = "活动"
        print("", activity_json["data"]["address"])
        user_list = []
        user_count = int(len(activity_json["data"]["user_list"]))
        if user_count > 0:
            print("    用户列表", user_count)
        for i in range(user_count):
            user_dict = {}
            user_id = activity_json["data"]["user_list"][i]["user_id"]
            avatar = activity_json["data"]["user_list"][i]["avatar"]
            user_name = activity_json["data"]["user_list"][i]["user_name"]
            user_dict["user_id"] = user_id
            user_dict["avatar"] = avatar
            user_dict["user_name"] = user_name
            user_list.append(user_dict)
        base["user_list"] = user_list

        tags_list = []
        tags_count = int(len(activity_json["data"]["tags"]))
        if tags_count > 0:
            print("    标签列表", tags_count)
        for j in range(tags_count):
            tags_dict = {}
            tag_id = activity_json["data"]["tags"][j]["tag_id"]
            name = activity_json["data"]["tags"][j]["name"]
            color = activity_json["data"]["tags"][j]["color"]
            tags_dict["tag_id"] = tag_id
            tags_dict["name"] = name
            tags_dict["color"] = color
            tags_list.append(tags_dict)
        base["tags"] = tags_list

        print("组装成功的json数据", str(base).replace("'", '"'))
        print("")


if __name__ == '__main__':
    activity_data_capture_qdy()
