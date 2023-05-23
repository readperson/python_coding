import requests
import json
from tools.json_data_handle import data_lens
from tools.json_data_handle import json_data_handle
from tools.response_api import response_api
from pp_physical_culture.scoreboard_data import scoreboard_data
from pp_physical_culture.scoreborad_information import scoreborad_information
from pp_physical_culture.scoreboard_schedule import scoreboard_schedule
from pp_physical_culture.scoreboard_TeamPlayer import scoreboard_TeamPlayer
from pp_physical_culture.players_list import players_list
from pp_physical_culture.team_List import team_list


# pp体育 数据 积分榜
def scoreboard():
    seasonId_list = [1759, 1769, 1770, 1755, 1750]
    competitionId_list = [5, 4, 7, 6, 9]
    type_list = ["英超", "西甲", "意甲", "德甲", "法甲"]
    index = 1
    try:
        for i in range(int(len(seasonId_list))):

            url = "https://sportdatax.suning.com/sdfocus-web/client/dataChannelRanks/getMatchScoreRanks/" + str(
                competitionId_list[index]) + "/" + str(
                seasonId_list[index]) + "/1001.htm?_source=ppsports&apptype=android&appversion=5.29&seasonId=" + str(
                seasonId_list[index]) + "&scoreBoardType=1001&competitionId=" + str(competitionId_list[index])
            # print(url)
            res_text = requests.get(url)
            res_text = json.loads(res_text.text)
            # print(res_text)
            data_dict = {}
            data_dict["type"] = type_list[index]
            data_dict["seasonId"] = seasonId_list[index]
            data_dict["competitionId"] = competitionId_list[index]
            bas_list = []
            noGroupRankList = data_lens(res_text["data"]["stageRankList"][0]["data"]["noGroupRankList"])

            noGroupRankList_list = ["colorDescription", "descriptionBackColor", "descriptionBackColorFrameNew",
                                    "descriptionBackColorNew", "descriptionBackColorNewV2"]
            for nlc in range(noGroupRankList):
                base = json_data_handle(res_text["data"]["stageRankList"][0]["data"]["noGroupRankList"], nlc,
                                        noGroupRankList_list)
                # print("base", base)
                rank_List = ["codeStage", "codeTeam", "drawNum", "goalsNum", "loseGoalsNum", "loseNum", "matchNum",
                             "rank",
                             "ranksColor", "ranksColorNew",
                             "ranksColorNewV2", "score", "stageId", "stageName", "teamId", "teamLogo", "teamName",
                             "updateTime", "winNum",
                             "winNum"]
                rankList_count = data_lens(
                    res_text["data"]["stageRankList"][0]["data"]["noGroupRankList"][nlc]["rankList"])
                rankList = []
                for r_c in range(rankList_count):
                    rankList_dict = json_data_handle(
                        res_text["data"]["stageRankList"][0]["data"]["noGroupRankList"][nlc]["rankList"], r_c,
                        rank_List)
                    rankList.append(rankList_dict)
                    # 数据
                    scoreboard_data(str(rankList_dict["teamId"]))
                    # 资讯
                    scoreborad_information(str(rankList_dict["teamId"]))
                    # 赛程
                    scoreboard_schedule(str(rankList_dict["teamId"]))
                    # 球员
                    scoreboard_TeamPlayer(str(rankList_dict["teamId"]))
                base["rankList"] = rankList
                bas_list.append(base)
            data_dict["data"] = bas_list
            response_api("/sszqbf/save_jifenbang_qiuduiliebiao", data_dict)
            # print("data_dict", data_dict)
            # 'type': '意甲', 'seasonId': 1770, 'competitionId': 7,
            # 球员榜
            players_list(data_dict["type"], data_dict["seasonId"], data_dict["competitionId"])
            # 球队榜
            team_list(data_dict["type"], data_dict["seasonId"], data_dict["competitionId"])
            index += 1
            # print("")
    except Exception as e:
        print("index======================", index)
        print(e)


if __name__ == '__main__':
    scoreboard()
