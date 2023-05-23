from tools.headers import headers_header
import json
import requests


def events_json(matchId,):
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    print("赛况")
    events_url = "https://mobile-gate.611.com/api/LiveDetail"
    events_data = {"MatchID": str(matchId), "SportType": "1", "ModeType": "9", "minTime": ""}
    events_headers = {
        "source": source,
        "lytime": lytime,
        "deviceid": deviceid,
        "deviceaid": deviceaid,
        "requestRam": requestRam,
        "sign": sign
    }
    events_rep = requests.post(url=events_url, data=events_data, headers=events_headers).text
    events_rep = json.loads(events_rep)
    # 定义一个list 天津比分统计
    events_list = {}
    for e in range(int(len(events_rep["data"]["modeData"]["listData"]))):
        events_sectionName = events_rep["data"]["modeData"]["listData"][e]["sectionName"]
        if events_sectionName == "比分统计":
            # data["score_statistics_name"] = "积分榜"

            competetionSituation_list = []
            competetionSituation_count = int(len(
                events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"]))
            if competetionSituation_count > 0:
                print("  比分统计")
            for i in range(competetionSituation_count):
                competetionSituation_dict = {}
                id = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"][
                        i][
                        "teamModel"]["id"]
                name = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"][
                        i][
                        "teamModel"]["name"]
                leagueMatchData = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"][
                        i][
                        "leagueMatchData"][0]
                competetionSituation_dict["id"] = id
                competetionSituation_dict["name"] = name
                competetionSituation_dict["leagueMatchData"] = leagueMatchData
                competetionSituation_list.append(competetionSituation_dict)
            events_list["score_statistics"] = competetionSituation_list

        if events_sectionName == "本场最佳":
            # data["best_all_name"] = "本场最佳"
            # print("  本场最佳")
            best_of_all = int(
                len(events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["courseBetter"]))
            if best_of_all > 0:
                print("  本场最佳")
            best_list = []
            for best_count in range(best_of_all):
                # print("  本场最佳",best_count)

                best_dict = {}
                technologyName = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["courseBetter"][
                        best_count][
                        "technologyName"]
                home_header_logo = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["courseBetter"][
                        best_count][
                        "home"]["logo"]
                home_name = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["courseBetter"][
                        best_count][
                        "home"]["name"]
                homeTechnologyDes = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["courseBetter"][
                        best_count][
                        "homeTechnologyDes"]
                away_header_logo = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["courseBetter"][
                        best_count][
                        "away"]["logo"]
                away_name = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["courseBetter"][
                        best_count][
                        "away"]["name"]
                awayTechnologyDes = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["courseBetter"][
                        best_count][
                        "awayTechnologyDes"]
                best_dict["technologyName"] = technologyName
                best_dict["home_header_logo"] = home_header_logo
                best_dict["home_name"] = home_name
                best_dict["homeTechnologyDes"] = homeTechnologyDes
                best_dict["away_header_logo"] = away_header_logo
                best_dict["away_name"] = away_name
                best_dict["awayTechnologyDes"] = awayTechnologyDes
                best_list.append(best_dict)
            events_list["best_of_all"] = best_list

        if events_sectionName == "球队统计":
            # data["team_statistics_name"] = "球队统计"

            analysis_list = []
            analysis_count = int(len(
                events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["teamTechnologyAnalysis"]))
            if analysis_count > 0:
                print("  球队统计")
            for als in range(analysis_count):

                analysis_dict = {}
                technologyName = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                        "teamTechnologyAnalysis"][
                        als]["technologyName"]

                if "homeTechnologyDes" in events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                    "teamTechnologyAnalysis"][als]:
                    homeTechnologyDes = events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                        "teamTechnologyAnalysis"][als]["homeTechnologyDes"]

                else:
                    homeTechnologyDes = events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                        "teamTechnologyAnalysis"][als].setdefault("homeTechnologyDes", "0")

                if "awayTechnologyDes" in events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                    "teamTechnologyAnalysis"][als]:
                    awayTechnologyDes = events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                        "teamTechnologyAnalysis"][als]["awayTechnologyDes"]

                else:
                    awayTechnologyDes = events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                        "teamTechnologyAnalysis"][als].setdefault("awayTechnologyDes", "0")
                analysis_dict["technologyName"] = technologyName
                analysis_dict["homeTechnologyDes"] = homeTechnologyDes
                analysis_dict["awayTechnologyDes"] = awayTechnologyDes
                analysis_list.append(analysis_dict)
            events_list["teamTechnologyAnalysis"] = analysis_list

        if events_sectionName == "球员统计":
            # data["player_statistics_name"] = "球员统计"
            qy_count = int(
                len(events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"]))
            if qy_count > 0:
                print("  球员统计")
            events_playerAnalysis = []
            for playerAnalysis_count in range(qy_count):

                #     if "id" in events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"][playerAnalysis_count]:
                id = events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"][
                    playerAnalysis_count]["teamModel"]["id"]

                # if "name" in events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"][playerAnalysis_count]:
                name = events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"][
                    playerAnalysis_count]["teamModel"]["name"]
                leagueMatchRightHeader = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"][
                        playerAnalysis_count]["leagueMatchRightHeader"]

                playerAnalysis_dict = {}
                playerAnalysis_dict["id"] = id
                playerAnalysis_dict["name"] = name
                playerAnalysis_dict["leagueMatchRightHeader"] = leagueMatchRightHeader

                eagueMatch_list = []
                for le_List in range(int(len(
                        events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"][
                            playerAnalysis_count]["leagueMatchLeftList"]))):
                    eagueMatch_dict = {}
                    le_List_id = \
                        events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"][
                            playerAnalysis_count]["leagueMatchLeftList"][le_List]["id"]
                    le_List_name = \
                        events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"][
                            playerAnalysis_count]["leagueMatchLeftList"][le_List]["name"]
                    le_List_fs = \
                        events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["playerAnalysis"][
                            playerAnalysis_count]["leagueMatchRightList"][le_List]
                    le_fs_list = []
                    for fs_count in range(int(len(le_List_fs))):
                        fs_list = str(le_List_fs[fs_count]).replace("'", "").replace('"', "")
                        le_fs_list.append(fs_list)
                    # print(len(le_List_fs))
                    eagueMatch_dict["id"] = le_List_id
                    eagueMatch_dict["name"] = le_List_name
                    eagueMatch_dict["match"] = le_fs_list
                    eagueMatch_list.append(eagueMatch_dict)

                playerAnalysis_dict["eagueMatch"] = eagueMatch_list
                events_playerAnalysis.append(playerAnalysis_dict)
            events_list["playerAnalysis"] = events_playerAnalysis
    return events_list
