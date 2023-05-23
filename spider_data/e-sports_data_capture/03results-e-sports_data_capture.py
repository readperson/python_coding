import json
import requests
import time, datetime


def esprot_data_capture():
    # with open("header.txt", "r", encoding="utf-8")as f:
    #
    #     lines = f.readlines()
    #     for i in range(int(len(lines))):
    #         if i == 0:
    #             url = str(lines[i]).replace("\n", "")
    #         if i == 1:
    #             url_chat = str(lines[i]).replace("\n", "")
    #         if i == 2:
    #             url_data = str(lines[i]).replace("\n", "")
    #     # print(lines)

    # 全部 雷速体育
    i = 1
    for j in range(13):
        i = i + 1
        print(i)
        url = "https://app-gateway.leisu.com/v1/app/match/esports/lol/match_list?date=202011" + str(
            i) + "&n=2&auth_key=1605243521-0-0-5eb979ce532449218bcff0ecab053ef4"
        header = {
            "sn": "003dca5d",
            "device_id": "1507bfd3f77dfd86703",
            "aid": "c20964cf79411c67",
            "time": "1605087709",
            "sign": "87d71d96683addc09d11da5eef23658e",
            "cdid": "c387b94e-765f-30c7-857e-c1ca7fe0144a",
            "start": "1604299428"
        }
        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
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
            # user_count = base_result["data"]["user_count"]
            if "user_count" in base_result["data"]:
                user_count = base_result["data"]["user_count"]
            else:
                user_count = base_result["data"].setdefault("id", "0")
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
            base["come_from"] = "雷速体育"
            base["capture_time"] = capture_time
            base["capture_type"] = "电竞"

            # print(base)
            # match_id
            url_chat = "https://app-gateway.leisu.com/v1/app/chat/history?room_id=R4_1_" + str(
                match_id) + "&auth_key=1605243610-0-0-36038c56a3f6983c9eca0f91104f87c6"
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
                # print(result_chat["data"][chat_count])
                #        'uid': 3481327,
                # 		'name': '红中将军',
                # 		'content': '@YuTian哪里的推荐',
                # 		'lv': 17,
                # 		'time': 1605084910420,
                # 		'vip': 0,
                # 		'p': 1,
                # 		'avatar': 'https://cdn.leisu.com/user/avatar/2020/08/17/FqqQb8c9IT1prPsXGwAkBHpqBzf7',
                # 		'g': 0
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
            # https://app-gateway.leisu.com/v1/app/match/esports/lol/match_analysis?match_id=3532886&auth_key=1605090916-0-0-14c214cdbd1166da41daafc0c41997de
            url_data = "https://app-gateway.leisu.com/v1/app/match/esports/lol/match_analysis?match_id=" + str(
                match_id) + "&auth_key=1605243891-0-0-04480f8f70b5e00e0dbd898582393701"
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
            print("111", data_result)
            base["data"] = data_result["data"]

            base["chat"] = chat_list
            base1 = str(base).replace("'", '"')
            with open("sg_" + str(i) + "_" + str(match_id) + ".txt", "w", encoding="utf-8") as f:
                f.write(base1)
            print("组装成功的json数据：", base1)


if __name__ == '__main__':
    esprot_data_capture()

# https://app-gateway.leisu.com/v1/app/match/esports/lol/match_list?date=20201114&n=1&auth_key=1605235524-0-0-ad509c969df8840e8def4c37889226e5
# https://app-gateway.leisu.com/v1/app/chat/history?room_id=R4_1_3532879&auth_key=1605235654-0-0-c33047102a73f73d563d8f4c5fee5977
# https://app-gateway.leisu.com/v1/app/match/esports/lol/match_analysis?match_id=3532879&auth_key=1605235655-0-0-5d26754aa0542383ea89283b9d3e6e3d
