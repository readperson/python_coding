import sys
sys.path.append("/opt/data_captureAPP")
import json
import requests
import time
import datetime
from lxml import etree

# 羽毛球
def match_data_capture_bmb():
    now = int(time.time())
    print(now)
    print(1605599606821)
    # with open("url.txt", "r", encoding="utf-8") as f:
    #     url = f.read()
    # url status 1进行中,0报名中,4待开赛,已结束2,3全部
    page = 0
    for i in range(5):
        page = page + 1
        url = "http://api.snsports.cn/api/content/phone/GetBMMatchListByAreaId.json?pageSize=20&pageNum=" + str(
            page) + "&status=3&sportType=羽毛球&cityId=5643&appVersion=3.5.1&device=androidphone&timestamp=" + str(
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

            # 参数球队
            # http://api.snsports.cn/api/content/phone/GetBMMatchDetail.json?&matchId=12482&pageNum=1&appVersion=3.5.1&device=androidphone&timestamp=1605687606725&sign=8b777128fe7ae86b2395c89f655f635efc5224f9&apikey=7f4880f7ab5dd50d53
            teamList_url = "http://api.snsports.cn/api/content/phone/GetBMMatchDetail.json?&matchId=" + str(
                id) + "&pageNum=1&appVersion=3.5.1&device=androidphone&timestamp="+str(now)+"725&sign=8b777128fe7ae86b2395c89f655f635efc5224f9&apikey=7f4880f7ab5dd50d53"
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
            # https://api.snsports.cn/api/content/phone/GetBMTeamScores.json?matchId=12269&pageSize=1000&device=phone&appVersion=3.2
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
                # 净胜局
                netWinGameStageCount = rep_score["messages"]["data"]["teamScores"][jf_cnt]["netWinGameStageCount"]
                # 净胜分
                netWinScoreCount = rep_score["messages"]["data"]["teamScores"][jf_cnt]["netWinScoreCount"]

                scoreboard_dict["groupName"] = groupName
                scoreboard_dict["name"] = name
                scoreboard_dict["badge"] = badge
                scoreboard_dict["totalRound"] = totalRound
                scoreboard_dict["winRound"] = winRound
                scoreboard_dict["netWinGameStageCount"] = netWinGameStageCount
                scoreboard_dict["netWinScoreCount"] = netWinScoreCount
                scoreboard_list.append(scoreboard_dict)
            # print("scoreboard_list:", scoreboard_list)
            base["scoreboard"] = scoreboard_list

            # 赛程表
            # https://api.snsports.cn/api/content/phone/GetBMGamesByBMMatchId.json?matchId=12512&device=phone&appVersion=3.2
            # https://api.snsports.cn/api/content/phone/GetBMGamesByBMMatchId.json?matchId=12269&device=phone&appVersion=3.2
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

            # https://www.snsports.cn/webapp/main-94c1161b60.html#/match-info?matchId=12443
            # event_Information_url = "https://www.snsports.cn/webapp/main-94c1161b60.html#/match-info?matchId=" + str(id)
            # session = requests.session()
            # response = session.get(event_Information_url)
            # html_str = response.content.decode("utf-8")
            # html = etree.HTML(html_str)
            # div_count = int(html.xpath('count(/html/body/div[1]/div/div/div)'))
            # print("---------------", div_count)

            # ,"status":0
            baseinfo = str(base).replace("'", '"')
            print("组装成功的json数据", baseinfo)
            print()


if __name__ == '__main__':
    match_data_capture_bmb()
