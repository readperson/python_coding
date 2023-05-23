import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from tools.base64_text import text_conversion_base64
from tools.response_api import response_api


# 一起浪电竞 训练比赛 赛事列表
def training_competition():
    url = "https://yql-service.e7lang.com/api/app/training?showToast=function+(t)%7Bs.showToastWithIcon(t)%7D&game=HPJY&page=1&size=10&successData=function+(t)%7Bvar+o%3Dn.props,s%3Do.pageSize,l%3Do.setCurrentData%3Bn.setState(%7BcurrentData:t,haveInit:!0%7D),1%3D%3D%3Dn.page%3F(n.state.isNoMoreData%3Dt.length%3Cs,n.setState(%7Bdata:t,refreshing:!1,isNoMoreData:t.length%3Cs%7D),l%26%26l(t)):(n.state.isNoMoreData%3Dt.length%3Cs,n.loadMoreing%3D!1,n.setState(%7Bdata:n.state.data.concat(t),isNoMoreData:t.length%3Cs,loadMoreing:!1,refreshing:!1%7D),l%26%26l(n.state.data.concat(t)))%7D"
    result = requests.get(url=url).text
    result = json.loads(result)
    result_count = int(len(result["data"]))
    for re_count in range(result_count):
        base = {}
        id = result["data"][re_count]["id"]
        brandId = result["data"][re_count]["brandId"]
        gameTheme = result["data"][re_count]["gameTheme"]
        HPJY = result["data"][re_count]["game"]
        gameStartTime = result["data"][re_count]["gameStartTime"]
        signUpStartTime = result["data"][re_count]["signUpStartTime"]
        signUpEndTime = result["data"][re_count]["signUpEndTime"]
        singUpQualifications = result["data"][re_count]["singUpQualifications"]
        base["id"] = id
        base["brandId"] = brandId
        base["gameTheme"] = gameTheme
        base["HPJY"] = HPJY
        base["gameStartTime"] = gameStartTime
        base["signUpStartTime"] = signUpStartTime
        base["signUpEndTime"] = signUpEndTime
        base["singUpQualifications"] = singUpQualifications
        print(gameTheme)

        # 比赛信息
        competition_information_dict = {}
        competition_information_url = "https://yql-service.e7lang.com/api/app/brand/" + str(brandId)
        competition_information = json.loads(requests.get(url=competition_information_url).text)
        bid = competition_information["id"]
        logo = competition_information["logo"]
        # base 64
        introduction = competition_information["introduction"]
        introduction = text_conversion_base64(introduction)
        createTime = competition_information["createTime"]
        randIndex = competition_information["randIndex"]
        memberNumber = competition_information["memberNumber"]
        competition_information_dict["id"] = bid
        competition_information_dict["logo"] = logo

        competition_information_dict["introduction"] = introduction
        competition_information_dict["createTime"] = createTime
        competition_information_dict["randIndex"] = randIndex
        competition_information_dict["memberNumber"] = memberNumber

        ompetition_information_url2 = "https://yql-service.e7lang.com/api/app/training/" + str(id)
        competition_information2 = json.loads(requests.get(url=ompetition_information_url2).text)
        communication = competition_information2["communication"]
        # base64
        gameRule = competition_information2["gameRule"]
        gameRule = text_conversion_base64(gameRule)
        trainningStatus = competition_information2["trainningStatus"]
        gameNum = competition_information2["gameNum"]
        singUpQualifications = competition_information2["singUpQualifications"]
        competition_information_dict["communication"] = communication
        competition_information_dict["gameRule"] = gameRule
        competition_information_dict["trainningStatus"] = trainningStatus
        competition_information_dict["gameNum"] = gameNum
        competition_information_dict["singUpQualifications"] = singUpQualifications
        base["competition_information"] = competition_information_dict

        # 战队报名
        battle_enroll_url = "https://yql-service.e7lang.com/api/app/training/" + str(id) + "/teams?state=PASS&size=25"
        battle_enroll_result = json.loads(requests.get(url=battle_enroll_url).text)
        battle_enroll_count = int(len(battle_enroll_result["data"]))
        if battle_enroll_count > 0:
            print("    战队报名", battle_enroll_count)
        battle_enroll_list = []
        for be_count in range(battle_enroll_count):
            battle_enroll_dict = {}
            beid = battle_enroll_result["data"][be_count]["id"]
            showId = battle_enroll_result["data"][be_count]["showId"]
            teamId = battle_enroll_result["data"][be_count]["teamId"]
            logo = battle_enroll_result["data"][be_count]["logo"]
            name = battle_enroll_result["data"][be_count]["name"]
            state = battle_enroll_result["data"][be_count]["state"]
            position = battle_enroll_result["data"][be_count]["position"]
            randIndex = battle_enroll_result["data"][be_count]["randIndex"]
            signUpTime = battle_enroll_result["data"][be_count]["signUpTime"]
            battle_enroll_dict["id"] = beid
            battle_enroll_dict["showId"] = showId
            battle_enroll_dict["teamId"] = teamId
            battle_enroll_dict["logo"] = logo
            battle_enroll_dict["name"] = name
            battle_enroll_dict["state"] = state
            battle_enroll_dict["position"] = position
            battle_enroll_dict["randIndex"] = randIndex
            battle_enroll_dict["signUpTime"] = signUpTime
            battle_enroll_list.append(battle_enroll_dict)
        base["battle_enroll"] = battle_enroll_list

        # 成绩排名
        score_ranking_url = "https://yql-service.e7lang.com/api/app/training/" + str(id) + "/grade?page=1&size=10"
        score_ranking = json.loads(requests.get(url=score_ranking_url).text)
        score_ranking_count = int(len(score_ranking["data"]))
        if score_ranking_count > 0:
            print("    成绩排名", score_ranking_count)
        score_ranking_list = []
        for sr_count in range(score_ranking_count):
            score_ranking_dict = {}
            showId = score_ranking["data"][sr_count]["showId"]
            name = score_ranking["data"][sr_count]["name"]
            totalIntegral = score_ranking["data"][sr_count]["totalIntegral"]
            whiteLogo = score_ranking["data"][sr_count]["whiteLogo"]
            blackLogo = score_ranking["data"][sr_count]["blackLogo"]
            totalKill = score_ranking["data"][sr_count]["totalKill"]
            totalRanking = score_ranking["data"][sr_count]["totalRanking"]
            chickens = score_ranking["data"][sr_count]["chickens"]
            score_ranking_dict["showId"] = showId
            score_ranking_dict["name"] = name
            score_ranking_dict["totalIntegral"] = totalIntegral
            score_ranking_dict["whiteLogo"] = whiteLogo
            score_ranking_dict["blackLogo"] = blackLogo
            score_ranking_dict["totalKill"] = totalKill
            score_ranking_dict["totalRanking"] = totalRanking
            score_ranking_dict["chickens"] = chickens
            performanceData_count = int(len(score_ranking["data"][sr_count]["performanceData"]))
            performanceData_list = []
            for p_count in range(performanceData_count):
                performanceData_dict = {}
                trainingId = score_ranking["data"][sr_count]["performanceData"][p_count]["trainingId"]
                teamKill = score_ranking["data"][sr_count]["performanceData"][p_count]["teamKill"]
                gameSequenceNo = score_ranking["data"][sr_count]["performanceData"][p_count]["gameSequenceNo"]
                killIntegral = score_ranking["data"][sr_count]["performanceData"][p_count]["killIntegral"]
                rankingIntegral = score_ranking["data"][sr_count]["performanceData"][p_count]["rankingIntegral"]
                ranking = score_ranking["data"][sr_count]["performanceData"][p_count]["ranking"]
                integral = score_ranking["data"][sr_count]["performanceData"][p_count]["integral"]
                performanceData_dict["trainingId"] = trainingId
                performanceData_dict["teamKill"] = teamKill
                performanceData_dict["gameSequenceNo"] = gameSequenceNo
                performanceData_dict["killIntegral"] = killIntegral
                performanceData_dict["rankingIntegral"] = rankingIntegral
                performanceData_dict["ranking"] = ranking
                performanceData_dict["integral"] = integral
                performanceData_list.append(performanceData_dict)

                score_ranking_dict["performanceData"] = performanceData_list
            score_ranking_list.append(score_ranking_dict)
        base["score_ranking"] = score_ranking_list


        url_club = "/esports/save_esports_match"
        response_api(url_club, base)


if __name__ == '__main__':
    training_competition()
