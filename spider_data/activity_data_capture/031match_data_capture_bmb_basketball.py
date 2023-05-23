import sys

sys.path.append("/opt/data_captureAPP")
import json
import requests
import time
import datetime
from tools.response_api import response_api


def match_data_capture_bmb():
    now = int(time.time())
    print(now)
    # with open("url.txt", "r", encoding="utf-8") as f:
    #     url = f.read()
    # url status 1进行中,0报名中,4待开赛,已结束2
    page = 0
    for i in range(5):
        page = page + 1
        url = "http://api.snsports.cn/api/content/phone/GetBMMatchListByAreaId.json?pageSize=20&pageNum=" + str(
            page) + "&status=3&sportType=篮球&cityId=5643&appVersion=3.5.1&device=androidphone&timestamp=" + str(
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
            print(rep["messages"]["data"]["otherMatchList"][rep_cnt])
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

            # 参赛球队
            # http://api.snsports.cn/api/content/phone/GetBMMatchDetail.json?&matchId=12482&pageNum=1&appVersion=3.5.1&device=androidphone&timestamp=1605687606725&sign=8b777128fe7ae86b2395c89f655f635efc5224f9&apikey=7f4880f7ab5dd50d53
            teamList_url = "http://api.snsports.cn/api/content/phone/GetBMMatchDetail.json?&matchId=" + str(
                id) + "&pageNum=1&appVersion=3.5.1&device=androidphone&timestamp=" + str(
                now) + "725&sign=8b777128fe7ae86b2395c89f655f635efc5224f9&apikey=7f4880f7ab5dd50d53"
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
                # 负
                rank = rep_score["messages"]["data"]["teamScores"][jf_cnt]["rank"]
                # 胜率
                winRate = rep_score["messages"]["data"]["teamScores"][jf_cnt]["winRate"]
                # 积分
                totalScore = rep_score["messages"]["data"]["teamScores"][jf_cnt]["totalScore"]
                # 均场得分
                avgWinScorePerGame = rep_score["messages"]["data"]["teamScores"][jf_cnt]["avgWinScorePerGame"]
                # 均场失分
                avgConcededScorePerGame = rep_score["messages"]["data"]["teamScores"][jf_cnt]["avgConcededScorePerGame"]
                # 均场净胜
                avgNetWinScorePerGame = rep_score["messages"]["data"]["teamScores"][jf_cnt]["avgNetWinScorePerGame"]
                scoreboard_dict["groupName"] = groupName
                scoreboard_dict["name"] = name
                scoreboard_dict["badge"] = badge
                scoreboard_dict["totalRound"] = totalRound
                scoreboard_dict["winRound"] = winRound
                scoreboard_dict["rank"] = rank
                scoreboard_dict["winRate"] = winRate
                scoreboard_dict["avgWinScorePerGame"] = avgWinScorePerGame
                scoreboard_dict["avgConcededScorePerGame"] = avgConcededScorePerGame
                scoreboard_dict["avgNetWinScorePerGame"] = avgNetWinScorePerGame
                scoreboard_list.append(scoreboard_dict)
            # print("scoreboard_list:", scoreboard_list)
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

            # 球员榜 得分 ball_players_list
            # score_account
            ball_players_list = {}

            score_account_url = "https://api.snsports.cn/api/content/phone/GetBMShooterScores.json?matchId=" + str(
                id) + "&pageSize=500&device=phone&appVersion=3.2"
            score_account_info = requests.get(score_account_url)
            score_account_info = json.loads(score_account_info.text)
            shooterScores_count = int(len(score_account_info["messages"]["data"]["shooterScores"]))
            if shooterScores_count > 0:
                print("  球员旁得分", shooterScores_count)
            shooterScores_list = []
            for s_count in range(shooterScores_count):
                shooterScores_dict = {}
                playerName = score_account_info["messages"]["data"]["shooterScores"][s_count]["playerName"]
                team_name = score_account_info["messages"]["data"]["shooterScores"][s_count]["team"]["name"]
                team_badge = score_account_info["messages"]["data"]["shooterScores"][s_count]["team"]["badge"]
                if team_badge.find("http") == -1:
                    team_badge = "http://images.snsports.cn/" + team_badge
                avgCount = score_account_info["messages"]["data"]["shooterScores"][s_count]["avgCount"]
                gameCount = score_account_info["messages"]["data"]["shooterScores"][s_count]["gameCount"]
                number = score_account_info["messages"]["data"]["shooterScores"][s_count]["number"]
                shooterScores_dict["playerName"] = playerName
                shooterScores_dict["team_name"] = team_name
                shooterScores_dict["team_badge"] = team_badge
                shooterScores_dict["avgCount"] = avgCount
                shooterScores_dict["gameCount"] = str(gameCount)
                shooterScores_dict["number"] = number
                shooterScores_list.append(shooterScores_dict)
            # print("shooterScores_list", shooterScores_list)
            ball_players_list["shooterScores"] = shooterScores_list

            # 助攻 holding_attack
            # https://api.snsports.cn/api/content/phone/GetBMAssisterScores.json?matchId=11944&pageSize=500&device=phone&appVersion=3.2
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

            # 篮板 backboard
            # https://api.snsports.cn/api/content/phone/GetBMRebounds.json?matchId=11944&pageSize=500&device=phone&appVersion=3.2
            backboard_url = "https://api.snsports.cn/api/content/phone/GetBMRebounds.json?matchId=" + str(
                id) + "&pageSize=500&device=phone&appVersion=3.2"
            backboard_info = requests.get(url=backboard_url)
            backboard_info = json.loads(backboard_info.text)
            backboard_count = int(len(backboard_info["messages"]["data"]["players"]))
            if backboard_count > 0:
                print("  球员旁篮板", backboard_count)
            backboard_list = []
            for b_count in range(backboard_count):
                backboard_dict = {}
                playerName = backboard_info["messages"]["data"]["players"][b_count]["playerName"]
                team_badge = backboard_info["messages"]["data"]["players"][b_count]["team"]["badge"]
                if team_badge.find("http") == -1:
                    team_badge = "http://images.snsports.cn/" + team_badge
                team_name = backboard_info["messages"]["data"]["players"][b_count]["team"]["name"]
                reboundCount = backboard_info["messages"]["data"]["players"][b_count]["reboundCount"]
                backboard_dict["playerName"] = playerName
                backboard_dict["team_badge"] = team_badge
                backboard_dict["team_name"] = team_name
                backboard_dict["reboundCount"] = reboundCount
                backboard_list.append(backboard_dict)
            # print("backboard_list", backboard_list)
            ball_players_list["backboard"] = backboard_list

            # intercept 抢断
            # https://api.snsports.cn/api/content/phone/GetBMSteals.json?matchId=11944&pageSize=500&device=phone&appVersion=3.2
            intercept_url = "https://api.snsports.cn/api/content/phone/GetBMSteals.json?matchId=" + str(
                id) + "&pageSize=500&device=phone&appVersion=3.2"
            intercept_info = requests.get(url=intercept_url)
            intercept_info = json.loads(intercept_info.text)
            intercept_count = int(len(intercept_info["messages"]["data"]["players"]))
            if intercept_count > 0:
                print("  球员抢断", intercept_count)
            intercept_list = []
            for i_count in range(intercept_count):
                intercept_dict = {}
                playerName = intercept_info["messages"]["data"]["players"][i_count]["playerName"]
                team_badge = intercept_info["messages"]["data"]["players"][i_count]["team"]["badge"]
                if team_badge.find("http") == -1:
                    team_badge = "http://images.snsports.cn/" + team_badge
                team_name = intercept_info["messages"]["data"]["players"][i_count]["team"]["name"]
                stealCount = intercept_info["messages"]["data"]["players"][i_count]["stealCount"]
                intercept_dict["playerName"] = playerName
                intercept_dict["team_badge"] = team_badge
                intercept_dict["team_name"] = team_name
                intercept_dict["stealCount"] = stealCount
                intercept_list.append(intercept_dict)
            # print(intercept_list)
            ball_players_list["intercept"] = intercept_list

            # 盖帽
            # https://api.snsports.cn/api/content/phone/GetBMBlocks.json?matchId=11944&pageSize=500&device=phone&appVersion=3.2
            block_shot_url = "https://api.snsports.cn/api/content/phone/GetBMBlocks.json?matchId=" + str(
                id) + "&pageSize=500&device=phone&appVersion=3.2"
            block_shot_info = requests.get(url=block_shot_url)
            block_shot_info = json.loads(block_shot_info.text)
            block_shot_count = int(len(block_shot_info["messages"]["data"]["players"]))
            if block_shot_count > 0:
                print("  球员盖帽", block_shot_count)
            block_shot_list = []
            for bs_count in range(block_shot_count):
                block_shot_dict = {}
                playerName = block_shot_info["messages"]["data"]["players"][bs_count]["playerName"]
                team_badge = block_shot_info["messages"]["data"]["players"][bs_count]["team"]["badge"]
                if team_badge.find("http") == -1:
                    team_badge = "http://images.snsports.cn/" + team_badge
                team_name = block_shot_info["messages"]["data"]["players"][bs_count]["team"]["name"]
                blockCount = block_shot_info["messages"]["data"]["players"][bs_count]["blockCount"]
                block_shot_dict["playerName"] = playerName
                block_shot_dict["team_badge"] = team_badge
                block_shot_dict["team_name"] = team_name
                block_shot_dict["blockCount"] = blockCount
                block_shot_list.append(block_shot_dict)
            # print("block_shot_list", block_shot_list)
            ball_players_list["block_shot"] = block_shot_list
            base["ball_players"] = ball_players_list

            # https://www.snsports.cn/webapp/main-94c1161b60.html#/match-info?matchId=12443
            # event_Information_url = "https://www.snsports.cn/webapp/main-94c1161b60.html#/match-info?matchId=" + str(id)
            # session = requests.session()
            # response = session.get(event_Information_url)
            # html_str = response.content.decode("utf-8")
            # html = etree.HTML(html_str)
            # div_count = int(html.xpath('count(/html/body/div[1]/div/div/div)'))
            # print("---------------", div_count)

            # ,"status":0

            print("组装成功的json:", str(base).replace("'", '"'))
            url_basketball = "/hotmatch/save_basketball"
            response_api(url_basketball, base)
            # headers_basketball = {"Content-Type": "application/json;charset=utf-8"}
            # data_basketball = json.dumps(base)
            # print("请求url:", url_basketball)
            # print("请求头:", headers_basketball)
            # print("请求数据:", data_basketball)
            # result_basketball = requests.post(url=url_basketball, headers=headers_basketball, data=data_basketball)
            # print("返回状态码：", result_basketball.status_code)
            # print("返回内容", result_basketball.text)
            # # base_info_list
            # # print("base:", base)
            # print("")
            #
            # print()


if __name__ == '__main__':
    match_data_capture_bmb()
