import sys

sys.path.append("/opt/data_captureAPP")
import json
import requests
import base64
from tools.response_api import response_api
from tools.time_treatment import now_time


# 一起浪电竞
# 俱乐部

def dragon_tigris():
    club_list_url = "https://yql-service.e7lang.com/api/app/clubs/trail-plans?trailPlanPageType=CLUB&size=500&page=1&game="
    club_list = requests.get(url=club_list_url)
    club_list = json.loads(club_list.text)
    # print("club_list:", club_list)
    cL_count = 1
    club_count = int(len(club_list["data"]))
    for c_count in range(club_count):
        print("共有俱乐部数据", club_count, "条，正在处理第", cL_count, "条数据,处理时间", now_time())
        cL_count = cL_count + 1
        base = {}
        price = club_list["data"][c_count]["price"]
        # 场
        times = club_list["data"][c_count]["times"]
        position = club_list["data"][c_count]["position"]
        clubId = club_list["data"][c_count]["clubId"]
        clubName = club_list["data"][c_count]["clubName"]
        # 点赞
        points = club_list["data"][c_count]["points"]
        age = club_list["data"][c_count]["age"]
        updateTime = str(club_list["data"][c_count]["updateTime"]).replace("T", " ")
        logoUrl = club_list["data"][c_count]["logoUrl"]
        address = club_list["data"][c_count]["address"]
        priority = club_list["data"][c_count]["priority"]
        label = club_list["data"][c_count]["label"]
        base["price"] = str(price)
        base["times"] = str(times)
        base["position"] = str(position)
        base["clubId"] = str(clubId)
        base["clubName"] = str(clubName)
        base["points"] = str(points)
        base["age"] = str(age)
        base["updateTime"] = updateTime
        base["logoUrl"] = logoUrl
        base["address"] = address
        base["priority"] = str(priority)
        base["label"] = str(label)
        base["label"] = str(label)
        base["label"] = str(label)
        base["label"] = str(label)
        import datetime
        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
        base["come_from"] = "一起浪电竞"
        base["capture_time"] = capture_time
        base["capture_type"] = "俱乐部"

        # 详细
        detailed_url = "https://yql-service.e7lang.com/api/app/clubs/" + str(clubId) + "/trail-plans"
        detailed = requests.get(url=detailed_url)
        detailed = json.loads(detailed.text)
        # print(detailed)
        print("clubName", clubName)
        if "code" in detailed:
            base["detailed"] = {}
        else:
            detailed_dict = {}
            demand = detailed["demand"]
            demand = base64.b64encode(demand.encode('utf-8'))
            demand = (str(demand, 'utf-8'))

            trailDate = detailed["trailDate"]
            beginTime = detailed["beginTime"]
            endTime = detailed["endTime"]
            imageUrl = detailed["imageUrl"]
            onlineState = detailed["onlineState"]
            trainGamePlan = detailed["trainGamePlan"]
            valuation = detailed["valuation"]
            if valuation is None:
                valuation = ""

            trainingNumber = detailed["trainingNumber"]
            if trainingNumber is None:
                trainingNumber = ""

            avgEliminate = detailed["avgEliminate"]
            if avgEliminate is None:
                avgEliminate = ""
            detailed_dict["demand"] = demand
            detailed_dict["trailDate"] = trailDate
            detailed_dict["beginTime"] = beginTime
            detailed_dict["endTime"] = endTime
            detailed_dict["imageUrl"] = imageUrl
            detailed_dict["onlineState"] = onlineState
            detailed_dict["trainGamePlan"] = trainGamePlan
            detailed_dict["valuation"] = valuation
            detailed_dict["trainingNumber"] = trainingNumber
            detailed_dict["avgEliminate"] = avgEliminate
            base["detailed"] = detailed_dict
        # 介绍
        introduce_url = "https://yql-service.e7lang.com/api/app/clubs/" + str(clubId)
        introduce = requests.get(url=introduce_url)
        introduce = json.loads(introduce.text)
        imageUrlList_count = int(len(introduce["imageUrlList"]))
        if imageUrlList_count == 0:
            continue
        introduce_dict = {}
        # introduction base64
        introduction = str(introduce["introduction"])
        introduction = base64.b64encode(introduction.encode('utf-8'))
        introduction = (str(introduction, 'utf-8'))
        coordinate = introduce["coordinate"]

        print("imageUrlList", len(introduce["imageUrlList"]))
        imageUrlList = introduce["imageUrlList"]
        detailAddress = introduce["detailAddress"]
        introduce_dict["introduction"] = introduction
        introduce_dict["coordinate"] = coordinate
        introduce_dict["imageUrlList"] = imageUrlList
        introduce_dict["detailAddress"] = detailAddress
        base["introduce"] = introduce_dict

        # 赛事历程
        course_events_url = "https://yql-service.e7lang.com/api/app/clubs/" + str(clubId) + "/race-courses"
        course_events = requests.get(url=course_events_url)
        course_events = json.loads(course_events.text)
        course_events = course_events["data"]
        base["course_events"] = course_events

        # 俱乐部战队
        battle_club_url = "https://yql-service.e7lang.com/api/app/teams?clubId=" + str(clubId)
        battle_club = json.loads(requests.get(url=battle_club_url).text)
        battle_count = int(len(battle_club["data"]))
        battle_club_list = []
        if battle_count > 0:
            print("    俱乐部战队", battle_count)
        for b_count in range(battle_count):
            battle_club_dict = {}
            id = battle_club["data"][b_count]["id"]
            showId = battle_club["data"][b_count]["showId"]
            blackLogo = battle_club["data"][b_count]["blackLogo"]
            whiteLogo = battle_club["data"][b_count]["whiteLogo"]
            name = battle_club["data"][b_count]["name"]
            declaration = battle_club["data"][b_count]["declaration"]
            businessValue = battle_club["data"][b_count]["businessValue"]
            createTime = battle_club["data"][b_count]["createTime"]
            battle_club_dict["id"] = id
            battle_club_dict["showId"] = showId
            battle_club_dict["blackLogo"] = blackLogo
            battle_club_dict["whiteLogo"] = whiteLogo
            battle_club_dict["name"] = name
            battle_club_dict["declaration"] = declaration
            battle_club_dict["businessValue"] = businessValue
            battle_club_dict["createTime"] = createTime
            battle_club_list.append(battle_club_dict)
        base["club_battle"] = battle_club_list

        url_club = "/esports/save_esports"
        response_api(url_club, base)


if __name__ == '__main__':
    dragon_tigris()
