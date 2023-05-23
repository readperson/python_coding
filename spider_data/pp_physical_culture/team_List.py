import requests
import json
from tools.json_data_handle import json_data_handle
from tools.response_api import response_api


## pp体育 数据 球队
def team_list(type_players, seasonId, competitionId):
    # itemCode 26进球 4封堵 5黄牌 6红牌 7射门 8射正 12越位 16犯规
    number = [26, 4, 5, 6, 7, 8, 12, 16]
    number_str = ["进球", "封堵", "黄牌", "红牌", "射门", "射正", "越位", "犯规"]
    # 'type': '意甲', 'seasonId': 1770, 'competitionId': 7,
    for index in range(int(len(number))):
        url = "https://sportdatax.suning.com/sdfocus-web/client/dataChannelRanks/getTeamRanks.do?" \
              "_source=ppsports&apptype=android&appversion=5.29&seasonId=" + str(seasonId) + "&itemCode=" + str(
            number[index]) + "&isAllFlag=1&competitionId=" + str(competitionId)
        res = requests.get(url)
        res = json.loads(res.text)
        # print(res)
        valueList_count = int(len(res["data"]["list"][0]["valueList"]))
        # "codeTeam": "C7T270",
        # "flag": "6",
        # "logoUrl": "http://image.suning.cn/uimg/SDSP/team/270.png?v=209912316666",
        # "rank": 1,
        # "statistic": "3",
        # "teamId": 270,
        # "teamLogo": "http://image.suning.cn/uimg/SDSP/team/270.png?v=209912316666",
        # "teamName":
        base = {}
        base["type_players"] = type_players
        base["seasonId"] = seasonId
        base["competitionId"] = competitionId
        base["itemCode"] = number[index]
        base["itemCode_name"] = number_str[index]
        valueList_index = ['codeTeam', 'flag', 'logoUrl', 'rank', 'statistic', 'teamId', 'teamLogo',
                           'teamName']
        value_List = []
        for v_c in range(valueList_count):
            value_List.append(json_data_handle(res["data"]["list"][0]["valueList"], v_c, valueList_index))
        base["valueList"] = value_List
        # for v_count in range(valueList_count):
        response_api("/sszqbf/save_qiuduibang", base)
        # print(base)


if __name__ == '__main__':
    team_list("英超", "1759", "5")
