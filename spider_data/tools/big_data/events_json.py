import requests
import json
from tools.headers import headers_header

# 赛况
def event_json(matchId):
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    print("赛况")
    events_url = "https://mobile-gate.611.com/api/LiveDetail"
    events_data = {"MatchID": str(matchId), "SportType": "0", "ModeType": "9", "minTime": ""}
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
    events_list = {}
    sj_count = int(len(events_rep["data"]["modeData"]["listData"]))

    for e in range(sj_count):
        events_sectionName = events_rep["data"]["modeData"]["listData"][e]["sectionName"]

        if events_sectionName == "实时指数":
            # real_time_index
            real_time_index = {}
            real_time_index["sectionName"] = "实时指数"
            atchCurrentOdds_count = int(len(events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"]))
            print("  实时指数", atchCurrentOdds_count)
            atchCurrentOdds_list = []
            for ao_count in range(atchCurrentOdds_count):
                atchCurrentOdds_dict = {}
                oddsName = events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsName"]
                atchCurrentOdds_dict["oddsName"] = oddsName
                oddsDatas_list = []
                oddsDatas_count = int(
                    len(events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"]))
                for odd_count in range(oddsDatas_count):
                    oddsDatas_dict = {}
                    timeElapsed = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "timeElapsed"]
                    homeScore = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "homeScore"]
                    awayScore = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "awayScore"]
                    stHome = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "stHome"]
                    stFlat = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "stFlat"]
                    stAway = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "stAway"]
                    instHome = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "instHome"]
                    if "instHomeRiseOrfall" in events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][odd_count]:
                        instHomeRiseOrfall = \
                            events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                                odd_count][
                                "instHomeRiseOrfall"]
                    else:
                        continue
                    instFlat = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "instFlat"]
                    instAway = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "instAway"]
                    instAwayRiseOrfall = \
                        events_rep["data"]["modeData"]["listData"][e]["matchCurrentOdds"][ao_count]["oddsDatas"][
                            odd_count][
                            "instAwayRiseOrfall"]
                    oddsDatas_dict["timeElapsed"] = timeElapsed
                    oddsDatas_dict["homeScore"] = homeScore
                    oddsDatas_dict["awayScore"] = awayScore
                    oddsDatas_dict["stHome"] = stHome
                    oddsDatas_dict["stFlat"] = stFlat
                    oddsDatas_dict["stAway"] = stAway
                    oddsDatas_dict["instHome"] = instHome
                    oddsDatas_dict["instHomeRiseOrfall"] = instHomeRiseOrfall
                    oddsDatas_dict["instFlat"] = instFlat
                    oddsDatas_dict["instAway"] = instAway
                    oddsDatas_dict["instAwayRiseOrfall"] = instAwayRiseOrfall
                    oddsDatas_list.append(oddsDatas_dict)
                atchCurrentOdds_dict["oddsDatas"] = oddsDatas_list
                atchCurrentOdds_list.append(atchCurrentOdds_dict)
                real_time_index["matchCurrentOdds"] = atchCurrentOdds_list
            events_list["real_time_index"] = real_time_index

        if events_sectionName == "事件":
            event = {}
            event["sectionName"] = "事件"
            sj_count2 = int(len(
                events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"]))
            if sj_count2 > 0:
                print("  事件", sj_count2)
            competetionSituation_list = []
            for csn in range(sj_count2):
                competetionSituation_dict = {}
                id = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"][
                        csn]["playerModel"]["id"]
                name = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"][
                        csn]["playerModel"]["name"]
                if "shirtNo" in events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                    "competetionSituation"][csn]["playerModel"]:
                    shirtNo = \
                        events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                            "competetionSituation"][
                            csn]["playerModel"]["shirtNo"]
                else:
                    shirtNo = \
                        events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                            "competetionSituation"][
                            csn]["playerModel"].setdefault("shirtNo", "")
                situationTime = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"][
                        csn]["situationTime"]
                situationDes = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"][
                        csn]["situationDes"]
                score = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"][
                        csn]["score"]
                competetionSituation_dict["pkey"] = id
                competetionSituation_dict["name"] = name

                competetionSituation_dict["shirtNo"] = shirtNo
                competetionSituation_dict["situationTime"] = str(situationTime)
                competetionSituation_dict["situationDes"] = situationDes
                competetionSituation_dict["score"] = score
                competetionSituation_list.append(competetionSituation_dict)
            event["competetionSituation"] = competetionSituation_list
            events_list["event"] = event

        if events_sectionName == "全场统计":
            # full_court_statistics
            #         teamsFromBothSidesData  competetionSituation
            full_court_statistics = {}
            full_court_statistics["sectionName"] = "全场统计"
            qctj_count = int(len(
                events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["teamTechnologyAnalysis"]))
            if qctj_count > 0:
                print("  全场统计", qctj_count)

            competetionSituation_list = []
            for tas in range(qctj_count):
                competetionSituation_dict = {}
                technologyName = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                        "teamTechnologyAnalysis"][
                        tas]["technologyName"]
                homeTechnologyDes = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                        "teamTechnologyAnalysis"][
                        tas]["homeTechnologyDes"]
                awayTechnologyDes = \
                    events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"][
                        "teamTechnologyAnalysis"][
                        tas]["awayTechnologyDes"]
                competetionSituation_dict["technologyName"] = technologyName
                competetionSituation_dict["homeTechnologyDes"] = homeTechnologyDes
                competetionSituation_dict["awayTechnologyDes"] = awayTechnologyDes
                competetionSituation_list.append(competetionSituation_dict)
            full_court_statistics["teamTechnologyAnalysis"] = competetionSituation_list
            events_list["full_court_statistics"] = full_court_statistics

    return events_list
