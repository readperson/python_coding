import requests
import json
from tools.headers import headers_header


def data_json(matchId,home_name,away_name):
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    print("数据")
    url_data = "https://mobile-gate.611.com/api/LiveDetail"
    data_data = {"MatchID": matchId, "SportType": "1", "ModeType": "13"}
    headers_data = {"source": source,
                    "lytime": lytime,
                    "deviceid": deviceid,
                    "deviceaid": deviceaid,
                    "requestRam": requestRam,
                    "sign": sign}
    rep_data = requests.post(url=url_data, data=data_data, headers=headers_data).text
    rep_data = json.loads(rep_data)
    # print(rep_data)

    data = {}
    for j in range(int(len(rep_data["data"]["modeData"]["listData"]))):

        # teamsFromBothSidesData
        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "球队概况":
            # data["team_profile"] = "球队概况"

            teams_base = {}
            home_name = \
                rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["homeTeamMsg"]["teamModel"][
                    "name"]
            away_name = \
                rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["awayTeamMsg"]["teamModel"][
                    "name"]

            team_count = int(len(
                rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["teamTechnologyAnalysis"]))
            team_list = []
            if team_count > 0:
                print("  球队概况")
            for t_count in range(team_count):
                team_dict = {}
                technologyName = \
                    rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["teamTechnologyAnalysis"][
                        t_count]["technologyName"]
                homeTechnologyDes = \
                    rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["teamTechnologyAnalysis"][
                        t_count]["homeTechnologyDes"]
                awayTechnologyDes = \
                    rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["teamTechnologyAnalysis"][
                        t_count]["awayTechnologyDes"]
                team_dict["technologyName"] = technologyName
                team_dict["homeTechnologyDes"] = homeTechnologyDes
                team_dict["awayTechnologyDes"] = awayTechnologyDes
                team_list.append(team_dict)
            teams_base["home_name"] = home_name
            teams_base["away_name"] = away_name
            teams_base["Analysis"] = team_list

            data["teamTechnologyAnalysis"] = teams_base
            # print(teams_base)

        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "场均数据对比":
            # data["comparison_field_data"] = "场均数据对比"

            comparison_base = {}
            home_name = \
                rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["homeTeamMsg"]["teamModel"][
                    "name"]
            away_name = \
                rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["awayTeamMsg"]["teamModel"][
                    "name"]

            comparison_count = int(len(
                rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["teamTechnologyAnalysis"]))
            if comparison_count > 0:
                print("  场均数据对比")
            comparison_list = []
            for com_count in range(comparison_count):
                comparison_dict = {}
                technologyName = \
                    rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["teamTechnologyAnalysis"][
                        com_count]["technologyName"]
                homeTechnologyDes = \
                    rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["teamTechnologyAnalysis"][
                        com_count]["homeTechnologyDes"]
                awayTechnologyDes = \
                    rep_data["data"]["modeData"]["listData"][j]["teamsFromBothSidesData"]["teamTechnologyAnalysis"][
                        com_count]["awayTechnologyDes"]
                comparison_dict["technologyName"] = technologyName
                comparison_dict["homeTechnologyDes"] = homeTechnologyDes
                comparison_dict["awayTechnologyDes"] = awayTechnologyDes
                comparison_list.append(comparison_dict)
            comparison_base["home_name"] = home_name
            comparison_base["away_name"] = away_name
            comparison_base["comparison"] = comparison_list
            data["comparison_field_data"] = comparison_base
            # print(comparison_base)

        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "历史交锋":

            # Historical_exchanges
            # data["history_name"] = "历史交锋"
            historical_exchanges = {}
            histroy_homeName = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][0]["teamName"]
            # 赢
            teamRecordWin = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][0]["teamRecordWin"]
            teamRecordWin = str(teamRecordWin)[0:1]
            # 平
            teamRecordTie = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][0]["teamRecordTie"]
            teamRecordTie = str(teamRecordTie)[0:1]
            # 输
            teamRecordLost = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][0]["teamRecordLost"]
            teamRecordLost = str(teamRecordLost)[0:1]
            textColorWin = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][0]["textColorWin"]
            textColorTie = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][0]["textColorTie"]
            textColorLost = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][0]["textColorLost"]
            competitionData = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][0]["competitionData"]
            if int(len(competitionData)) > 0:
                print("  历史交锋")
            historical_exchanges["histroy_homeName"] = histroy_homeName
            historical_exchanges["teamRecordWin"] = teamRecordWin
            historical_exchanges["teamRecordTie"] = teamRecordTie
            historical_exchanges["teamRecordLost"] = teamRecordLost
            historical_exchanges["textColorWin"] = textColorWin
            historical_exchanges["textColorTie"] = textColorTie
            historical_exchanges["textColorLost"] = textColorLost
            titionData_list = []
            for titionData_count in range(int(len(competitionData))):
                titionData_ls = \
                    rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][0]["competitionData"][
                        titionData_count]
                # ['韩篮甲', '2020-10-09', '客', '88-85', '主']
                # print(titionData_ls)
                # print(titionData_ls[2])

                titionData_single_list = []
                if titionData_ls[2] == "主":
                    titionData_single_list.append(titionData_ls[0])
                    titionData_single_list.append(titionData_ls[1])
                    titionData_single_list.append(home_name)
                    titionData_single_list.append(titionData_ls[3])
                    titionData_single_list.append(away_name)
                    titionData_single_list.append("主")
                    titionData_list.append(titionData_single_list)

                if titionData_ls[2] == "客":
                    titionData_single_list.append(titionData_ls[0])
                    titionData_single_list.append(titionData_ls[1])
                    titionData_single_list.append(away_name)
                    titionData_single_list.append(titionData_ls[3])
                    titionData_single_list.append(home_name)
                    titionData_single_list.append("客")
                    titionData_list.append(titionData_single_list)

            historical_exchanges["competitionData"] = titionData_list
            # print("historical_exchanges", historical_exchanges)
            data["historical_exchanges"] = historical_exchanges

            # team_list
        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "近期战绩":

            # leagueMatchList
            # recent_achievements
            ra_count = int(len(rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"]))
            if ra_count > 0:
                print("  近期战绩")
            recent_achievements_list = []
            for rac in range(ra_count):
                recent_achievements_dict = {}
                recent_home_name = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][rac]["teamName"]
                teamRecordWin = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][rac]["teamRecordWin"]
                teamRecordWin = str(teamRecordWin)[0:1]
                teamRecordTie = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][rac]["teamRecordTie"]
                teamRecordTie = str(teamRecordTie)[0:1]
                teamRecordLost = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][rac][
                    "teamRecordLost"]
                teamRecordLost = str(teamRecordLost)[0:1]
                textColorWin = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][rac]["textColorWin"]
                textColorTie = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][rac]["textColorTie"]
                textColorLost = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][rac]["textColorLost"]
                recent_achievements_dict["recent_home_name"] = recent_home_name
                recent_achievements_dict["teamRecordWin"] = teamRecordWin
                recent_achievements_dict["teamRecordTie"] = teamRecordTie
                recent_achievements_dict["teamRecordLost"] = teamRecordLost
                recent_achievements_dict["textColorWin"] = textColorWin
                recent_achievements_dict["textColorTie"] = textColorTie
                recent_achievements_dict["textColorLost"] = textColorLost
                ra_ct = int(
                    len(rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][rac]["competitionData"]))
                rac_list = []
                for ra_ctn in range(ra_ct):
                    rac_single_list = []
                    ra_ctn = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][rac]["competitionData"][
                        ra_ctn]
                    # ['菲篮杯', '2020-11-11', '客', '90-88', '凤凰燃料大师']
                    if ra_ctn[2] == "主":
                        rac_single_list.append(ra_ctn[0])
                        rac_single_list.append(ra_ctn[1])
                        rac_single_list.append(home_name)
                        rac_single_list.append(ra_ctn[3])
                        rac_single_list.append(ra_ctn[4])
                        rac_single_list.append("主")
                        rac_list.append(rac_single_list)
                    if ra_ctn[2] == "客":
                        rac_single_list.append(ra_ctn[0])
                        rac_single_list.append(ra_ctn[1])
                        rac_single_list.append(ra_ctn[4])
                        rac_single_list.append(ra_ctn[3])
                        rac_single_list.append(home_name)
                        rac_single_list.append("客")
                        rac_list.append(rac_single_list)
                recent_achievements_dict["competitionData"] = rac_list
                recent_achievements_list.append(recent_achievements_dict)
                data["recent_achievements_list"] = recent_achievements_list
                # print("recent_achievements_list:",recent_achievements_list)

        scoreboards = {}
        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "积分榜":
            # data["scoreboard_name"] = "积分榜"
            # sectionName = rep_data["data"]["modeData"]["listData"][j]["sectionName"]
            leagueMatchHeader = rep_data["data"]["modeData"]["listData"][j]["leagueMatchHeader"]
            scoreboards["leagueMatchHeader"] = leagueMatchHeader
            jf_count = int(len(rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"]))
            if jf_count > 0:
                print("  积分榜")
            scoreboards_data_List = []
            for k in range(jf_count):
                scoreboards_data_dict = {}
                teamId = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k]["teamId"]
                teamName = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k]["teamName"]
                leagueMatchData = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k][
                    "leagueMatchData"]
                scoreboards_data_dict["teamId"] = teamId
                scoreboards_data_dict["teamName"] = teamName
                scoreboards_data_dict["leagueMatchData"] = leagueMatchData
                scoreboards_data_List.append(scoreboards_data_dict)
                scoreboards["leagueMatchList"] = scoreboards_data_List
            data["scoreboards"] = scoreboards

        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "未来三场":
            # data["three_next_name"] = "积分榜"

            three_next_dict = {}
            # sectionName = rep_data["data"]["modeData"]["listData"][j]["sectionName"]

            leagueMatchList = []
            wlsc = int(len(rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"]))
            if wlsc > 0:
                print("  未来三场")
            for k in range(wlsc):
                three_next_dict1 = {}
                teamId = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k]["teamId"]
                teamName = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k]["teamName"]
                three_next_dict1["teamId"] = teamId
                three_next_dict1["teamName"] = teamName
                competitionDataOdds = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k][
                    "competitionDataOdds"]
                three_next_dict1["competitionDataOdds"] = competitionDataOdds

                # print("three_next_dict1", three_next_dict1)
                leagueMatchList.append(three_next_dict1)
                three_next_dict["leagueMatchList"] = leagueMatchList
                # print("three_next_dict", three_next_dict)
            data["three_next"] = three_next_dict
    return data
