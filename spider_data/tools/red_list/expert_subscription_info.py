import random
from tools.base64_text import text_conversion_base64
from tools.p_uid import p_uid
from tools.random_number import random_number


def expert_subscription_info(result, red_list_type, planList):
    person_info = {}
    mobile = result["result"]["expertBaseInfo"]["mobile"]
    expertsName = result["result"]["expertBaseInfo"]["expertsName"]
    expertDes = result["result"]["expertBaseInfo"]["expertDes"]
    totalFans = result["result"]["expertBaseInfo"]["totalFans"]
    expertsNickName = result["result"]["expertBaseInfo"]["expertsNickName"]
    headPortrait = result["result"]["expertBaseInfo"]["headPortrait"]
    # expertsIntroduction
    expertsIntroduction = result["result"]["expertBaseInfo"]["expertsIntroduction"]
    expertsIntroduction = text_conversion_base64(expertsIntroduction)
    expertMatch = result["result"]["expertBaseInfo"]["expertMatch"]
    expertTag = result["result"]["expertBaseInfo"]["expertTag"]
    person_info["mobile"] = mobile
    person_info["expertsName"] = expertsName
    person_info["type"] = red_list_type
    person_info["expertDes"] = expertDes
    person_info["totalFans"] = totalFans
    person_info["expertsNickName"] = expertsNickName
    person_info["headPortrait"] = headPortrait
    person_info["expertsIntroduction"] = expertsIntroduction
    person_info["expertMatch"] = expertMatch
    person_info["expertTag"] = expertTag
    print(expertsName)
    newPlanList_list = []
    person_info["redPlanList"] = newPlanList_list

    # ================================newPlanList1=======================================

    newPlanList_count1 = int(len(result["result"][planList]))
    if newPlanList_count1 > 0:
        print("    单关列表", newPlanList_count1)
    newPlanList_list1 = []
    for new_count1 in range(newPlanList_count1):
        newPlanList_dict1 = {}
        color_status = random.randint(1, 2)
        status = random.randint(1, 3)
        status = status
        color_status = color_status
        price = result["result"][planList][new_count1]["price"]
        vip_pric = price
        DATE_BEFORE = result["result"][planList][new_count1]["DATE_BEFORE"]
        # passType = result["result"]["newPlanList1"][new_count1]["passType"]
        recommendTitle = result["result"][planList][new_count1]["recommendTitle"]
        userName = expertsNickName
        recommendExplain = result["result"][planList][new_count1]["recommendExplain"]
        goldDiscountPrice = price
        newPlanList_dict1["pkey"] = p_uid() + random_number()
        newPlanList_dict1["color_status"] = color_status
        newPlanList_dict1["status"] = status
        newPlanList_dict1["vip_pric"] = vip_pric
        newPlanList_dict1["DATE_BEFORE"] = DATE_BEFORE
        newPlanList_dict1["passType"] = red_list_type
        newPlanList_dict1["recommendTitle"] = recommendTitle
        newPlanList_dict1["price"] = price
        newPlanList_dict1["userName"] = userName
        recommendExplain = text_conversion_base64(recommendExplain)
        newPlanList_dict1["recommendExplain"] = recommendExplain
        newPlanList_dict1["goldDiscountPrice"] = goldDiscountPrice

        matchs_count1 = int(len(result["result"][planList][new_count1]["matchs"]))
        matchs_list1 = []
        for m_count1 in range(matchs_count1):
            matchs_dict1 = {}
            matchTime = result["result"][planList][new_count1]["matchs"][m_count1][
                "matchTime"]
            leagueName = result["result"][planList][new_count1]["matchs"][m_count1][
                "leagueName"]
            recommendContent = result["result"][planList][new_count1]["matchs"][m_count1][
                "recommendContent"]
            homeLogo = result["result"][planList][new_count1]["matchs"][m_count1][
                "homeLogo"]
            awayName = result["result"][planList][new_count1]["matchs"][m_count1][
                "awayName"]
            awayLogo = result["result"][planList][new_count1]["matchs"][m_count1][
                "awayLogo"]
            homeName = result["result"][planList][new_count1]["matchs"][m_count1][
                "homeName"]
            matchesName = homeName + " VS " + awayName
            matchs_dict1["matchTime"] = matchTime
            matchs_dict1["leagueName"] = leagueName
            matchs_dict1["recommendContent"] = recommendContent
            matchs_dict1["homeLogo"] = homeLogo
            matchs_dict1["matchesName"] = matchesName
            matchs_dict1["awayName"] = awayName
            matchs_dict1["awayLogo"] = awayLogo
            matchs_dict1["homeName"] = homeName
            type_g = ["让球+2", "标赔", "让球+1"]
            tg = random.randint(0, int(len(type_g)) - 1)
            type_globe = type_g[tg]
            homewin = str(random.uniform(1, 5))[0:4]
            flat = str(random.uniform(1, 5))[0:4]
            awaywin = str(random.uniform(1, 5))[0:4]
            matchs_dict1["type_g"] = type_globe
            matchs_dict1["homewin"] = homewin
            matchs_dict1["flat"] = flat
            matchs_dict1["awaywin"] = awaywin
            matchs_list1.append(matchs_dict1)
        newPlanList_dict1["matchs"] = matchs_list1
        newPlanList_list1.append(newPlanList_dict1)
        person_info["redPlanList1"] = newPlanList_list1
    return person_info
