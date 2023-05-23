import requests
import json
from tools.json_data_handle import json_data_handle
from tools.response_api import response_api


# pp体育 数据模块 球员
def players_list(type_players, seasonId, competitionId):
    # 'type': '意甲', 'seasonId': 1770, 'competitionId': 7,
    # itemCode 3进球 4助攻 7射门 8射正 1出场 2首发 5黄牌 6红牌
    number_str = ["进球", "助攻", "射门", "射正", "出场", "首发", "黄牌", "红牌"]
    number = [3, 4, 7, 8, 1, 2, 5, 6]
    for index in range(int(len(number))):
        url = "https://sportdatax.suning.com/sdfocus-web/client/dataChannelRanks/getPlayerRanks.do?" \
              "_source=ppsports&apptype=android&appversion=5.29&seasonId=" + str(seasonId) + "&itemCode=" + str(
            number[index]) + "&isAllFlag=1&competitionId=" + str(competitionId)
        # print(url)
        res = requests.get(url)
        res = json.loads(res.text)
        # print(res)
        valueList_count = int(len(res["data"]["list"][0]["valueList"]))
        # "codePlayer": "C8T7883",
        # "playerId": 7883,
        # "playerLogo": "http://image.suning.cn/uimg/SDSP/player/7883.jpeg?v=1498717923043",
        # "playerName": "B·费尔南德斯",
        # "rank": 4,
        # "rankData": "11",
        # "teamId": 256,
        # "teamLogo": "http://image.suning.cn/uimg/SDSP/team/256.png?v=209912316666",
        # "teamName": "曼联"
        base = {}
        base["type_players"] = type_players
        base["seasonId"] = seasonId
        base["competitionId"] = competitionId
        base["itemCode"] = number[index]
        base["itemCode_name"] = number_str[index]
        valueList_index = ['codePlayer', 'playerId', 'playerLogo', 'playerName', 'rank', 'rankData', 'teamId',
                           'teamLogo', 'teamName']
        value_List = []
        for v_c in range(valueList_count):
            value_List.append(json_data_handle(res["data"]["list"][0]["valueList"], v_c, valueList_index))
        base["valueList"] = value_List
        # for v_count in range(valueList_count):
        # print("players_list", base)
        response_api("/sszqbf/save_qiuyuanbang", base)


if __name__ == '__main__':
    # 'type_players': '英超', 'seasonId': 1759, 'competitionId': 5, 'itemCode': 26
    players_list("英超", "1759", "5")
