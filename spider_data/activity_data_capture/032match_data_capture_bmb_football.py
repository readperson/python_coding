import sys

sys.path.append("/opt/data_captureAPP")
import json
import requests
import time
import datetime
from tools.response_api import response_api


def match_data_capture_bmb():
    now = int(time.time())
    # print(now)
    # print(1605599606821)
    # with open("url.txt", "r", encoding="utf-8") as f:
    #     url = f.read()
    # url status 1进行中,0报名中,4待开赛,已结束2
    page = 0
    for i in range(5):
        page = page + 1
        url = "http://api.snsports.cn/api/content/phone/GetBMMatchListByAreaId.json?pageSize=20&pageNum=" + str(
            page) + "&status=3&sportType=足球&cityId=5643&appVersion=3.5.1&device=androidphone&timestamp=" + str(
            now) + "366&sign=675dd63f978ff2feeb2928b647c63c89a0caf843&apikey=7f4880f7ab5dd50d53"
        rep = requests.get(url=url)
        rep = json.loads(rep.text)
        # print("rep:", rep)
        # # "state":  0 报名中 1 待开赛 2 进行中 3 已结束
        rep_count = int(len(rep["messages"]["data"]["otherMatchList"]))
        number_s = 0
        for rep_cnt in range(rep_count):
            number_s = number_s + 1
            print("正在爬取第", page, "页的第", number_s, "条数据")
            base = {}
            # print(rep["messages"]["data"]["otherMatchList"][rep_cnt])
            chineseName = rep["messages"]["data"]["otherMatchList"][rep_cnt]["chineseName"]
            if int(len(chineseName)) < 5:
                print(chineseName, "chineseName 小于五个字符长度放弃")
                continue
            icon = rep["messages"]["data"]["otherMatchList"][rep_cnt]["icon"]
            if icon.find("http") == -1:
                icon = "http://images.snsports.cn/" + icon
            id = rep["messages"]["data"]["otherMatchList"][rep_cnt]["id"]
            gameType = rep["messages"]["data"]["otherMatchList"][rep_cnt]["gameType"]
            beginDate = rep["messages"]["data"]["otherMatchList"][rep_cnt]["beginDate"]
            # 2020-11-14T00:00:00+0800
            beginDate = str(beginDate).replace("T", " ").split("+0")[0]
            endDate = rep["messages"]["data"]["otherMatchList"][rep_cnt]["endDate"]
            endDate = str(endDate).replace("T", " ").split("+0")[0]
            sportType = rep["messages"]["data"]["otherMatchList"][rep_cnt]["sportType"]
            stateDesc = rep["messages"]["data"]["otherMatchList"][rep_cnt]["stateDesc"]
            base["city"] = rep["messages"]["data"]["otherMatchList"][rep_cnt]["city"]
            if "district" in rep["messages"]["data"]["otherMatchList"][rep_cnt]:
                base["district"] = rep["messages"]["data"]["otherMatchList"][rep_cnt]["district"]
            else:
                base["district"] = {}
            state = rep["messages"]["data"]["otherMatchList"][rep_cnt]["state"]
            base["chineseName"] = chineseName
            base["icon"] = icon
            base["id"] = id
            base["gameType"] = gameType
            base["beginDate"] = beginDate
            base["endDate"] = endDate
            base["sportType"] = sportType
            base["stateDesc"] = stateDesc
            base["state"] = state
            capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
            base["come_from"] = "斑马邦"
            base["capture_time"] = capture_time
            base["capture_type"] = "赛事"
            print(chineseName, sportType)

            # http://api.snsports.cn/api/content/phone/GetBMMatchDetail.json?&matchId=12512&pageNum=1&appVersion=3.5.1&device=androidphone&timestamp=1605619033954&sign=5f82602dc74b0b343fa1312ee051a132a420057d&apikey=7f4880f7ab5dd50d53
            url_image = "http://api.snsports.cn/api/content/phone/GetBMMatchDetail.json?&matchId=" + str(
                id) + "&pageNum=1&appVersion=3.5.1&device=androidphone&timestamp=" + str(
                now) + "954&sign=5f82602dc74b0b343fa1312ee051a132a420057d&apikey=7f4880f7ab5dd50d53"
            image_info = requests.get(url=url_image)
            image_info = json.loads(image_info.text)
            backgroundImage = image_info["messages"]["data"]["match"]["backgroundImage2"]
            if backgroundImage.find("http") == -1:
                backgroundImage = "http://images.snsports.cn/" + backgroundImage

            base["backgroundImage"] = backgroundImage

            # teamList 参数球队
            # http://api.snsports.cn/api/content/phone/GetBMMatchDetail.json?&matchId=12512&pageNum=1&appVersion=3.5.1&device=androidphone&timestamp=1605683528249&sign=2167705e46274103578f4923beca454c82597430&apikey=7f4880f7ab5dd50d53
            teamList_url = "http://api.snsports.cn/api/content/phone/GetBMMatchDetail.json?&matchId=" + str(
                id) + "&pageNum=1&appVersion=3.5.1&device=androidphone&timestamp=" + str(
                now) + "249&sign=2167705e46274103578f4923beca454c82597430&apikey=7f4880f7ab5dd50d53"
            teamList_info = requests.get(url=teamList_url)
            teamList_info = json.loads(teamList_info.text)
            teamList_count = int(len(teamList_info["messages"]["data"]["teamList"]))
            if teamList_count > 0:
                print("  参赛球队", teamList_count)
            teamList_list = []
            for te_cnt in range(teamList_count):
                teamList_dict = {}
                badge = teamList_info["messages"]["data"]["teamList"][te_cnt]["badge"]
                if badge.find("http") == -1:
                    badge = "http://images.snsports.cn/" + badge
                groupName = teamList_info["messages"]["data"]["teamList"][te_cnt]["groupName"]
                name = teamList_info["messages"]["data"]["teamList"][te_cnt]["name"]
                location = teamList_info["messages"]["data"]["teamList"][te_cnt]["location"]
                teamList_dict["badge"] = badge
                teamList_dict["groupName"] = groupName
                teamList_dict["name"] = name
                teamList_dict["location"] = location
                teamList_list.append(teamList_dict)
            base["teamList"] = teamList_list

            # 积分榜
            # http://api.snsports.cn/api/content/phone/GetBMMatchDetail.json?&matchId=12512&pageNum=1&appVersion=3.5.1&device=androidphone&timestamp=1605594526099&sign=56d5d7e32586f8142e23dbf022c5d02523ff125f&apikey=7f4880f7ab5dd50d53
            score_url = "https://api.snsports.cn/api/content/phone/GetBMTeamScores.json?matchId=" + str(
                id) + "&pageSize=1000&device=phone&appVersion=3.2"
            rep_score = requests.get(url=score_url)
            rep_score = json.loads(rep_score.text)
            # print("rep_info",rep_info)
            jfb_count = int(len(rep_score["messages"]["data"]["teamScores"]))
            if jfb_count > 0:
                print("  积分榜", jfb_count)
            scoreboard_list = []
            for jf_cnt in range(jfb_count):
                scoreboard_dict = {}
                # print(rep_score["messages"]["data"]["teamScores"][jf_cnt])
                groupName = rep_score["messages"]["data"]["teamScores"][jf_cnt]["groupName"]
                name = rep_score["messages"]["data"]["teamScores"][jf_cnt]["name"]
                badge = rep_score["messages"]["data"]["teamScores"][jf_cnt]["badge"]
                if badge.find("http") == -1:
                    badge = "http://images.snsports.cn/" + badge
                # 赛
                totalRound = rep_score["messages"]["data"]["teamScores"][jf_cnt]["totalRound"]
                # 胜
                winRound = rep_score["messages"]["data"]["teamScores"][jf_cnt]["winRound"]
                # 平
                tieRound = rep_score["messages"]["data"]["teamScores"][jf_cnt]["tieRound"]
                # 输
                loseRound = rep_score["messages"]["data"]["teamScores"][jf_cnt]["loseRound"]
                # 进/失
                goalCount = rep_score["messages"]["data"]["teamScores"][jf_cnt]["goalCount"]
                concededCount = rep_score["messages"]["data"]["teamScores"][jf_cnt]["concededCount"]
                goal_conceded = str(goalCount) + "/" + str(concededCount)
                totalScore = rep_score["messages"]["data"]["teamScores"][jf_cnt]["totalScore"]
                scoreboard_dict["groupName"] = groupName
                scoreboard_dict["name"] = name
                scoreboard_dict["badge"] = badge
                scoreboard_dict["totalRound"] = totalRound
                scoreboard_dict["winRound"] = winRound
                scoreboard_dict["tieRound"] = tieRound
                scoreboard_dict["loseRound"] = loseRound
                scoreboard_dict["goal_conceded"] = goal_conceded
                scoreboard_dict["totalScore"] = totalScore
                scoreboard_list.append(scoreboard_dict)
            base["scoreboard"] = scoreboard_list

            # 赛程表
            # https://api.snsports.cn/api/content/phone/GetBMGamesByBMMatchId.json?matchId=12512&device=phone&appVersion=3.2
            schedule_url = "https://api.snsports.cn/api/content/phone/GetBMGamesByBMMatchId.json?matchId=" + str(
                id) + "&round=1&isGroupRound=1&device=phone&appVersion=3.2"
            schedule_info = requests.get(url=schedule_url)
            schedule_info = json.loads(schedule_info.text)
            schedule_count = int(len(schedule_info["messages"]["data"]["games"]))
            if schedule_count > 0:
                print("  赛程表", schedule_count)
            schedule_list = []
            for s_count in range(schedule_count):
                schedule_dict = {}
                # print(schedule_info["messages"]["data"]["games"][s_count])
                homeTeam = {}
                home_name = schedule_info["messages"]["data"]["games"][s_count]["homeTeam"]["name"]
                home_badge = schedule_info["messages"]["data"]["games"][s_count]["homeTeam"]["badge"]
                if home_badge.find("http") == -1:
                    home_badge = "http://images.snsports.cn/" + home_badge
                homeScore = schedule_info["messages"]["data"]["games"][s_count]["homeScore"]
                homeTeam["home_name"] = home_name
                homeTeam["home_badge"] = home_badge
                homeTeam["homeScore"] = str(homeScore)
                schedule_dict["homeTeam"] = homeTeam
                statusLabel = schedule_info["messages"]["data"]["games"][s_count]["liveStatus"]["statusLabel"]
                status = schedule_info["messages"]["data"]["games"][s_count]["liveStatus"]["status"]
                schedule_dict['statusLabel'] = statusLabel
                schedule_dict['status'] = status

                awayTeam = {}
                way_name = schedule_info["messages"]["data"]["games"][s_count]["awayTeam"]["name"]
                away_badge = schedule_info["messages"]["data"]["games"][s_count]["awayTeam"]["badge"]
                if away_badge.find("http") == -1:
                    away_badge = "http://images.snsports.cn/" + away_badge
                awayScore = schedule_info["messages"]["data"]["games"][s_count]["awayScore"]
                awayTeam["way_name"] = way_name
                awayTeam["away_badge"] = away_badge
                awayTeam["awayScore"] = str(awayScore)
                schedule_dict["awayTeam"] = awayTeam
                schedule_list.append(schedule_dict)
            # print("schedule_list:", schedule_list)
            base["schedule"] = schedule_list

            # 球员榜 射手 ball_players_list
            ball_players_list = {}
            players_shooter_url = "https://api.snsports.cn/api/content/phone/GetBMShooterScores.json?matchId=" + str(
                id) + "&pageSize=500&device=phone&appVersion=3.2"
            players_shooter_info = requests.get(url=players_shooter_url)
            players_shooter_info = json.loads(players_shooter_info.text)
            players_shooter_count = int(len(players_shooter_info["messages"]["data"]["shooterScores"]))
            if players_shooter_count > 0:
                print("  球员榜射手", players_shooter_count)
            players_shooter_list = []
            for players_cnt in range(players_shooter_count):
                players_shooter_dict = {}
                # print(players_info["messages"]["data"]["shooterScores"][players_cnt])
                playerName = players_shooter_info["messages"]["data"]["shooterScores"][players_cnt]["playerName"]
                number = players_shooter_info["messages"]["data"]["shooterScores"][players_cnt]["number"]
                # 进球数 排名
                goalCount = players_shooter_info["messages"]["data"]["shooterScores"][players_cnt]["goalCount"]
                team_name = players_shooter_info["messages"]["data"]["shooterScores"][players_cnt]["team"]["name"]
                team_badge = players_shooter_info["messages"]["data"]["shooterScores"][players_cnt]["team"]["badge"]
                if team_badge.find("http") == -1:
                    team_badge = "http://images.snsports.cn/" + team_badge

                players_shooter_dict["playerName"] = playerName
                players_shooter_dict["number"] = number
                players_shooter_dict["goalCount"] = goalCount
                players_shooter_dict["team_name"] = team_name
                players_shooter_dict["team_badge"] = team_badge
                players_shooter_list.append(players_shooter_dict)
            # print("players_shooter_list 射手", players_shooter_list)
            ball_players_list["players_shooter_list"] = players_shooter_list

            # 红黄  reddish_yellow
            # https://api.snsports.cn/api/content/phone/GetRedOrYellowCardByBMMatchId.json?bmMatchId=12480&device=phone&appVersion=3.2
            reddish_yellow_url = "https://api.snsports.cn/api/content/phone/GetRedOrYellowCardByBMMatchId.json?bmMatchId=" + str(
                id) + "&device=phone&appVersion=3.2"
            reddish_yellow_info = requests.get(url=reddish_yellow_url)
            reddish_yellow_info = json.loads(reddish_yellow_info.text)
            r_y_teams_count = int(len(reddish_yellow_info["messages"]["data"]["teams"]))
            if r_y_teams_count > 0:
                print("  球员红黄队", r_y_teams_count)
            y_r = {}
            reddish_yellow_list_team = []
            for r_y_t_cnt in range(r_y_teams_count):
                reddish_yellow_dict_team = {}
                r_y_team_name = reddish_yellow_info["messages"]["data"]["teams"][r_y_t_cnt]["name"]
                r_y_teamId = reddish_yellow_info["messages"]["data"]["teams"][r_y_t_cnt]["teamId"]
                r_y_team_badge = reddish_yellow_info["messages"]["data"]["teams"][r_y_t_cnt]["badge"]
                if r_y_team_badge.find("http") == -1:
                    r_y_team_badge = "http://images.snsports.cn/" + r_y_team_badge
                r_y_team_yellowCount = reddish_yellow_info["messages"]["data"]["teams"][r_y_t_cnt]["yellowCount"]
                r_y_team_redCount = reddish_yellow_info["messages"]["data"]["teams"][r_y_t_cnt]["redCount"]
                r_y_team_totalCount = reddish_yellow_info["messages"]["data"]["teams"][r_y_t_cnt]["totalCount"]
                reddish_yellow_dict_team["team_name"] = r_y_team_name
                reddish_yellow_dict_team["teamId"] = r_y_teamId
                reddish_yellow_dict_team["team_badge"] = r_y_team_badge
                reddish_yellow_dict_team["yellowCount"] = r_y_team_yellowCount
                reddish_yellow_dict_team["redCount"] = r_y_team_redCount
                reddish_yellow_dict_team["totalCount"] = r_y_team_totalCount
                reddish_yellow_list_team.append(reddish_yellow_dict_team)
            y_r["teams"] = reddish_yellow_list_team

            r_y_p_count = int(len(reddish_yellow_info["messages"]["data"]["players"]))
            if r_y_p_count > 0:
                print("  球员红黄队员", r_y_p_count)
            reddish_yellow_ryp_list = []
            for ryp_count in range(r_y_p_count):
                reddish_yellow_ryp_dict = {}
                r_y_playerName = reddish_yellow_info["messages"]["data"]["players"][ryp_count]["playerName"]
                r_y_teamId1 = reddish_yellow_info["messages"]["data"]["players"][ryp_count]["teamId"]
                r_y_team_name = reddish_yellow_info["messages"]["data"]["players"][ryp_count]["team"]["name"]
                r_y_yellowCount = reddish_yellow_info["messages"]["data"]["players"][ryp_count]["yellowCount"]
                r_y_redCardCount = reddish_yellow_info["messages"]["data"]["players"][ryp_count]["redCardCount"]
                r_y_totalCount = reddish_yellow_info["messages"]["data"]["players"][ryp_count]["totalCount"]
                reddish_yellow_ryp_dict["playerName"] = r_y_playerName
                reddish_yellow_ryp_dict["teamId"] = r_y_teamId1
                reddish_yellow_ryp_dict["teamName"] = r_y_team_name
                reddish_yellow_ryp_dict["yellowCount"] = r_y_yellowCount
                reddish_yellow_ryp_dict["redCardCount"] = r_y_redCardCount
                reddish_yellow_ryp_dict["totalCount"] = r_y_totalCount
                reddish_yellow_ryp_list.append(reddish_yellow_ryp_dict)
            y_r["players"] = reddish_yellow_ryp_list
            ball_players_list["reddish_yellow_list"] = y_r

            # 助攻holding attack
            # https://api.snsports.cn/api/content/phone/GetBMAssisterScores.json?matchId=12237&pageSize=500&device=phone&appVersion=3.2
            holding_attack_url = "https://api.snsports.cn/api/content/phone/GetBMAssisterScores.json?matchId=" + str(
                id) + "&pageSize=500&device=phone&appVersion=3.2"
            holding_attack_info = requests.get(url=holding_attack_url)
            holding_attack_info = json.loads(holding_attack_info.text)
            assisterScores_count = int(len(holding_attack_info["messages"]["data"]["assisterScores"]))
            if assisterScores_count > 0:
                print("  球员旁助攻", assisterScores_count)
            assisterScores_list = []
            for a_count in range(assisterScores_count):
                assisterScores_dict = {}
                playerName = holding_attack_info["messages"]["data"]["assisterScores"][a_count]["playerName"]
                team_badge = holding_attack_info["messages"]["data"]["assisterScores"][a_count]["team"]["badge"]
                if team_badge.find("http") == -1:
                    team_badge = "http://images.snsports.cn/" + team_badge
                team_name = holding_attack_info["messages"]["data"]["assisterScores"][a_count]["team"]["name"]
                assistCount = holding_attack_info["messages"]["data"]["assisterScores"][a_count]["assistCount"]
                assisterScores_dict["playerName"] = playerName
                assisterScores_dict["team_badge"] = team_badge
                assisterScores_dict["team_name"] = team_name
                assisterScores_dict["assistCount"] = assistCount
                assisterScores_list.append(assisterScores_dict)
            # print("assisterScores_list", assisterScores_list)
            ball_players_list["assisterScores"] = assisterScores_list
            base["ball_players"] = ball_players_list

            # https://www.snsports.cn/webapp/main-94c1161b60.html#/match-info?matchId=12443
            # event_Information_url = "https://www.snsports.cn/webapp/main-94c1161b60.html#/match-info?matchId=" + str(id)
            # session = requests.session()
            # response = session.get(event_Information_url)
            # html_str = response.content.decode("utf-8")
            # html = etree.HTML(html_str)
            # div_count = int(html.xpath('count(/html/body/div[1]/div/div/div)'))
            # print("---------------", div_count)

            print("组装成功的json:", str(base).replace("'", '"'))
            url_football = "/hotmatch/save_football"
            response_api(url_football, base)
            # headers_football = {"Content-Type": "application/json;charset=utf-8"}
            # data_football = json.dumps(base)
            # print("请求url:", url_football)
            # print("请求头:", headers_football)
            # print("请求数据:", data_football)
            # result_basketball = requests.post(url=url_football, headers=headers_football, data=data_football)
            # print("返回状态码：", result_basketball.status_code)
            # print("返回内容", result_basketball.text)
            # # base_info_list
            # # print("base:", base)
            # print("")


if __name__ == '__main__':
    match_data_capture_bmb()
