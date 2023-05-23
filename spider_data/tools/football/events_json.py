import requests
import json
from tools.headers import headers_header


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
    # print("events_rep--:", events_rep)
    events_list = {}
    sj_count = int(len(events_rep["data"]["modeData"]["listData"]))

    for e in range(sj_count):
        events_sectionName = events_rep["data"]["modeData"]["listData"][e]["sectionName"]
        if events_sectionName == "事件":

            #         teamsFromBothSidesData  competetionSituation
            competetionSituation_list = []
            sj_count2 = int(len(
                events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"]))
            if sj_count2:
                print("  事件")
            for csn in range(sj_count2):
                # print("competetionSituation",events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["competetionSituation"][csn])
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
                competetionSituation_dict["id"] = id
                competetionSituation_dict["name"] = name
                # if name == "":
                #     continue

                competetionSituation_dict["shirtNo"] = shirtNo
                competetionSituation_dict["situationTime"] = str(situationTime)
                competetionSituation_dict["situationDes"] = situationDes
                competetionSituation_dict["score"] = score
                competetionSituation_list.append(competetionSituation_dict)
            events_list["competetionSituation"] = competetionSituation_list

        if events_sectionName == "全场统计":
            #         teamsFromBothSidesData  competetionSituation
            qctj_count = int(len(
                events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["teamTechnologyAnalysis"]))
            if qctj_count > 0:
                print("  全场统计")

            competetionSituation_list = []
            for tas in range(qctj_count):
                competetionSituation_dict = {}
                # print("-----",events_rep["data"]["modeData"]["listData"][e]["teamsFromBothSidesData"]["teamTechnologyAnalysis"][tas])
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
            events_list["teamTechnologyAnalysis"] = competetionSituation_list
    return events_list
