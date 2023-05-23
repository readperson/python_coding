import sys

sys.path.append("/opt/data_captureAPP")
import json
import requests
import time, datetime
from tools.response_api import response_api
from tools.handl_specialcharacters import hzs_sub


# 约战广场
def warfare_platform():
    now = int(time.time())
    url_list = "http://api.snsports.cn/api/content/phone/GetBMPKSubjectList.json?pageSize=20&pageNum=1&cityId=5643&sportType=%E8%B6%B3%E7%90%83&appVersion=3.5.1&device=androidphone&timestamp=" + str(
        now) + "742&sign=2ba0bcca0638da5afc1d71c0ae02085144fde2cc&apikey=7f4880f7ab5dd50d53"
    result_list = requests.get(url=url_list)
    result_list = json.loads(result_list.text)
    # print("result_list:", result_list)
    result_count = int(len(result_list["messages"]["data"]["subjects"]))
    for res_count in range(result_count):
        base = {}
        title = result_list["messages"]["data"]["subjects"][res_count]["title"]
        print(title)
        createDate = result_list["messages"]["data"]["subjects"][res_count]["createDate"]
        createDate = str(createDate).replace("T", " ").split("+0")[0]
        id = result_list["messages"]["data"]["subjects"][res_count]["id"]
        homeTeamId = result_list["messages"]["data"]["subjects"][res_count]["homeTeamId"]
        venueId = result_list["messages"]["data"]["subjects"][res_count]["venueId"]
        beginDate = result_list["messages"]["data"]["subjects"][res_count]["beginDate"]
        beginDate = str(beginDate).replace("T", " ").split("+0")[0]
        beginDate = str(beginDate).replace("T", " ").split("+0")[0]
        # b_data = beginDate.split(" ")[1].split(":")[0]
        endDate = result_list["messages"]["data"]["subjects"][res_count]["endDate"]
        endDate = str(endDate).replace("T", " ").split("+0")[0]
        # e_data = endDate.split(" ")[1].split(":")[0]
        # ee_data = endDate.split(" ")[0].split("-")[1]
        # eee_data = endDate.split(" ")[0].split("-")[2]

        sportType = result_list["messages"]["data"]["subjects"][res_count]["sportType"]
        gameType = result_list["messages"]["data"]["subjects"][res_count]["gameType"]
        costDesc = result_list["messages"]["data"]["subjects"][res_count]["costDesc"]
        venueName = result_list["messages"]["data"]["subjects"][res_count]["venueName"]
        homeTeam_name = result_list["messages"]["data"]["subjects"][res_count]["homeTeam"]["name"]
        homeTeam_badge = result_list["messages"]["data"]["subjects"][res_count]["homeTeam"]["badge"]
        if homeTeam_badge.find("http") == -1:
            homeTeam_badge = "http://images.snsports.cn/" + homeTeam_badge
        location = result_list["messages"]["data"]["subjects"][res_count]["location"]
        # print(result_list["messages"]["data"]["subjects"][res_count])
        latitude = result_list["messages"]["data"]["subjects"][res_count]["latitude"]
        longitude = result_list["messages"]["data"]["subjects"][res_count]["longitude"]
        base["title"] = title
        base["createDate"] = createDate
        base["id"] = id
        base["homeTeamId"] = homeTeamId
        base["venueId"] = venueId
        base["beginDate"] = beginDate
        base["endDate"] = endDate
        base["sportType"] = sportType
        base["gameType"] = gameType
        base["costDesc"] = costDesc
        base["venueName"] = venueName
        base["homeTeam_name"] = homeTeam_name
        base["homeTeam_badge"] = homeTeam_badge
        base["location"] = location
        base["latitude"] = latitude
        base["longitude"] = longitude

        base["come_from"] = "斑马邦"
        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
        base["capture_time"] = capture_time
        base["capture_type"] = "赛事"

        # 查看球队详情
        # http://api.snsports.cn/api/content/phone/GetBMTeamDetailV2.json?teamId=&passport=ijhe6ombkdk4ln5rqhuicbc8zcer3or6&appVersion=3.5.1&device=androidphone&timestamp=1605755536431&sign=0fdede4d77974a200122296984c9e6cc3bd30042&apikey=7f4880f7ab5dd50d53
        team_details_url = "http://api.snsports.cn/api/content/phone/GetBMTeamDetailV2.json?teamId=" + homeTeamId + "&passport=ijhe6ombkdk4ln5rqhuicbc8zcer3or6&appVersion=3.5.1&device=androidphone&timestamp=" + str(
            now) + "431&sign=0fdede4d77974a200122296984c9e6cc3bd30042&apikey=7f4880f7ab5dd50d53"
        team_details = requests.get(url=team_details_url)
        team_details = json.loads(team_details.text)
        print("team_details:", team_details)
        games_count = int(len(team_details["messages"]["data"]["games"]))
        data = {}
        gameCount = team_details["messages"]["data"]["gameCount"]
        winCount = team_details["messages"]["data"]["winCount"]
        flatCount = 0
        loseCount = team_details["messages"]["data"]["loseCount"]
        #
        data["gameCount"] = gameCount
        data["winCount"] = winCount
        data["flatCount"] = flatCount
        data["loseCount"] = loseCount
        games_list = []
        if games_count > 0:
            print("  查看球队详情", games_count)
        for g_count in range(games_count):
            games_dict = {}
            homeTeamId = team_details["messages"]["data"]["games"][g_count]["homeTeam"]["id"]
            homeTeam_name = team_details["messages"]["data"]["games"][g_count]["homeTeam"]["name"]
            homeTeam_badge = team_details["messages"]["data"]["games"][g_count]["homeTeam"]["badge"]
            if homeTeam_badge.find("http") == -1:
                homeTeam_badge = "http://images.snsports.cn/" + homeTeam_badge

            if "homeScore" in team_details["messages"]["data"]["games"][g_count]:
                homeScore = team_details["messages"]["data"]["games"][g_count]["homeScore"]
            else:
                homeScore = team_details["messages"]["data"]["games"][g_count].setdefault("homeScore", 0)

            awayTeamId = team_details["messages"]["data"]["games"][g_count]["awayTeam"]["id"]
            awayTeam_name = team_details["messages"]["data"]["games"][g_count]["awayTeam"]["name"]
            awayTeam_badge = team_details["messages"]["data"]["games"][g_count]["awayTeam"]["badge"]
            if awayTeam_badge.find("http") == -1:
                awayTeam_badge = "http://images.snsports.cn/" + awayTeam_badge
            if "awayScore" in team_details["messages"]["data"]["games"][g_count]:
                awayScore = team_details["messages"]["data"]["games"][g_count]["awayScore"]
            else:
                awayScore = team_details["messages"]["data"]["games"][g_count].setdefault("awayScore", 0)

            games_dict["homeTeamId"] = homeTeamId
            games_dict["homeTeam_name"] = homeTeam_name
            games_dict["homeTeam_badge"] = homeTeam_badge
            games_dict["homeScore"] = str(homeScore)
            games_dict["awayTeamId"] = awayTeamId
            games_dict["awayTeam_name"] = awayTeam_name
            games_dict["awayScore"] = str(awayScore)
            games_list.append(games_dict)
        data["games"] = games_list
        # 球员
        # http://api.snsports.cn/api/content/phone/GetBMTeamUserList.json?teamId=277854&pageSize=1000&temporary=1&passport=ijhe6ombkdk4ln5rqhuicbc8zcer3or6&appVersion=3.5.1&device=androidphone&timestamp=1605789865355&sign=502b8c5dcb22ba08cd699ec3efc7183490bdfea5&apikey=7f4880f7ab5dd50d53
        player_user_url = "http://api.snsports.cn/api/content/phone/GetBMTeamUserList.json?teamId=" + str(
            homeTeamId) + "&pageSize=1000&temporary=1&passport=ijhe6ombkdk4ln5rqhuicbc8zcer3or6&appVersion=3.5.1&device=androidphone&timestamp=" + str(
            now) + "355&sign=502b8c5dcb22ba08cd699ec3efc7183490bdfea5&apikey=7f4880f7ab5dd50d53"
        player_user_info = requests.get(url=player_user_url)
        player_user_info = json.loads(player_user_info.text)
        player_user_count = int(len(player_user_info["messages"]["data"]["players"]))
        player_user_list = []
        if player_user_count > 0:
            print("  球员", player_user_count)
        for pu_count in range(player_user_count):
            player_user_dict = {}
            number = player_user_info["messages"]["data"]["players"][pu_count]["number"]
            role = player_user_info["messages"]["data"]["players"][pu_count]["role"]
            nickName = player_user_info["messages"]["data"]["players"][pu_count]["nickName"]
            avatar = player_user_info["messages"]["data"]["players"][pu_count]["avatar"]
            if avatar.find("http") == -1:
                avatar = "http://images.snsports.cn/" + avatar
            position = player_user_info["messages"]["data"]["players"][pu_count]["position"]
            player_user_dict["number"] = number
            player_user_dict["role"] = role
            player_user_dict["nickName"] = hzs_sub(nickName)
            player_user_dict["avatar"] = avatar
            player_user_dict["position"] = position
            player_user_list.append(player_user_dict)
        data["player_user"] = player_user_list
        base["data"] = data

        battle_url = "/hotmatch/save_battle"

        response_api(battle_url, base)


if __name__ == '__main__':
    warfare_platform()
