import json
import requests
import time, datetime


def esprot_data_capture():

    # 全部 雷速体育
    url = "https://app-gateway.leisu.com/v1/app/match/esports/lol/match_live?auth_key=1605174247-0-0-7e3215dfd94ca83ad13755d886333794"
    url = url
    header = {
        "sn": "003dca5d",
        "device_id": "1507bfd3f77dfd86703",
        "aid": "c20964cf79411c67",
        "time": "1605087709",
        "sign": "87d71d96683addc09d11da5eef23658e",
        "cdid": "c387b94e-765f-30c7-857e-c1ca7fe0144a",
        "start": "1604299428"
    }

    base_result = requests.get(url=url, headers=header).text
    base_result = json.loads(base_result)
    print(base_result)
    base = {}
    for base_count in range(int(len(base_result["data"]["matches"]))):
        # print(base_result["data"]["matches"][base_count])
        # 'match_time': 1605081600,
        # 			'id': 3532886,
        match_id = base_result["data"]["matches"][base_count]["id"]
        print(match_id)
        match_time = base_result["data"]["matches"][base_count]["match_time"]
        timeArray = time.localtime(match_time)
        match_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        status = base_result["data"]["matches"][base_count]["status_id"]
        if "id" in base_result["data"]["matches"][base_count]["home"]:
            home_id = base_result["data"]["matches"][base_count]["home"]["id"]
        else:
            home_id = base_result["data"]["matches"][base_count]["home"].setdefault("id", "0")

        home_name = base_result["data"]["matches"][base_count]["home"]["name"]
        home_score = base_result["data"]["matches"][base_count]["home"]["score"]
        home_logo = base_result["data"]["matches"][base_count]["home"]["logo"]
        if "stats" in base_result["data"]["matches"][base_count]["home"]:
            home_stats = base_result["data"]["matches"][base_count]["home"]["stats"]
        else:
            home_stats = base_result["data"]["matches"][base_count]["home"].setdefault("stats", "[]")

        if "id" in base_result["data"]["matches"][base_count]["away"]:
            away_id = base_result["data"]["matches"][base_count]["away"]["id"]
        else:
            away_id = base_result["data"]["matches"][base_count]["away"].setdefault("id", "0")
        away_name = base_result["data"]["matches"][base_count]["away"]["name"]
        away_score = base_result["data"]["matches"][base_count]["away"]["score"]
        away_logo = base_result["data"]["matches"][base_count]["away"]["logo"]
        if "stats" in base_result["data"]["matches"][base_count]["away"]:
            away_stats = base_result["data"]["matches"][base_count]["away"]["stats"]
        else:
            away_stats = base_result["data"]["matches"][base_count]["away"].setdefault("stats", "[]")
        # timeStamp = 1381419600
        #  3 timeArray = time.localtime(timeStamp)
        #  4 otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        #  5 print(otherStyleTime)
        user_count = base_result["data"]["user_count"]
        match_id = str(match_id)
        base["id"] = str(match_id)
        base["match_time"] = match_time
        base["status"] = str(status)

        base["home_id"] = str(home_id)
        base["home_name"] = home_name
        base["home_score"] = str(home_score)
        base["home_logo"] = home_logo
        base["home_stats"] = home_stats

        base["away_id"] = str(away_id)
        base["away_name"] = away_name
        base["away_score"] = str(away_score)
        base["away_logo"] = away_logo
        base["away_stats"] = away_stats
        base["user_count"] = user_count

        # print(base)

        url_chat = "https://app-gateway.leisu.com/v1/app/chat/history?room_id=R4_1_3532888&auth_key=1605174280-0-0-88b858077e56cd5644c6d99bdf677358"
        header_chat = {
            "sn": "003dca5d",
            "device_id": "1507bfd3f77dfd86703",
            "aid": "c20964cf79411c67",
            "time": "1605090558",
            "sign": "8d84ade2abc47cf4f2a7411920326af2",
            "cdid": "c387b94e-765f-30c7-857e-c1ca7fe0144a",
            "start": "1604299428"
        }
        result_chat = requests.get(url=url_chat, headers=header_chat).text
        result_chat = json.loads(result_chat)
        # print(result_chat)

        chat_list = []
        for chat_count in range(int(len(result_chat["data"]))):
            chat_dict = {}
            uid = result_chat["data"][chat_count]["uid"]
            name = result_chat["data"][chat_count]["name"]
            content = result_chat["data"][chat_count]["content"]
            lv = result_chat["data"][chat_count]["lv"]
            avatar = result_chat["data"][chat_count]["avatar"]
            chat_dict["uid"] = uid
            chat_dict["name"] = name
            chat_dict["content"] = content
            chat_dict["lv"] = lv
            chat_dict["avatar"] = avatar
            chat_list.append(chat_dict)
        base["chat"] = chat_list

        # 数据
        url_data = "https://app-gateway.leisu.com/v1/app/match/esports/lol/match_analysis?match_id=3532886&auth_key=1605090916-0-0-14c214cdbd1166da41daafc0c41997de"
        url_data = url_data
        header_data = {
            "sn": "003dca5d",
            "device_id": "1507bfd3f77dfd86703",
            "aid": "c20964cf79411c67",
            "time": "1605090558",
            "sign": "8d84ade2abc47cf4f2a7411920326af2",
            "cdid": "c387b94e-765f-30c7-857e-c1ca7fe0144a",
            "start": "1604299428"
        }
        data_result = requests.get(url=url_data, headers=header_data).text
        data_result = json.loads(data_result)
        # print("111",data_result["data"])
        base["data"]=data_result["data"]


        base["chat"] = chat_list
        print("组装成功的json数据：", str(base).replace("'", '"'))


if __name__ == '__main__':
    esprot_data_capture()
