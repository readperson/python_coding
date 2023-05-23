import sys

sys.path.append("/opt/data_captureAPP")
from football_pitch_lyc.football_tools.match.match_details.headers_json import headers_json
from tools.requests_api import requests_api
from tools.json_package.json_package import json_package
from football_pitch_lyc.football_tools.match.matchid_return_list import matchid_return_list
from tools.response_api import response_api


# 观众席 - 动态 matchid
def dynamic():
    matchid_list = matchid_return_list()
    matchid_count = int(len(matchid_list))
    for m_c in range(matchid_count):
        print("共有动态数据：", matchid_count, "条", "正在处理", m_c + 1, "条")
        matchid = matchid_list[m_c]
        # print(matchid)
        url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
        data = 'json={"uid":-1,"method":"common_topic_getActivityTopicList","activityId":' + matchid + ',"activityType":31,"page":1,"limit":10,"version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"a16a8536a0690ec2a01566f0adf40a32eaaf285c"}'
        headers = headers_json()
        rep = requests_api(url=url, headers=headers, data=data)
        rep_count = int(len(rep["returndata"]["topicData"]))

        for r_count in range(rep_count):
            base = {}
            base["matchId"] = matchid
            if "homeTeamId" in rep["returndata"]["topicData"][r_count]["matchInfo"]:
                print("---------企业---------")
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "gameName", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "Comment", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "targetName", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "userName", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "publish_time", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "browserNumber", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "targetPortrait", "0", base)
                # 这里的matchId 有关联关系
                json_package(rep["returndata"]["topicData"][r_count], "matchId", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "homeTeamId", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "awayTeamId", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "homeName", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "awayName", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "homeIcon", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "awayIcon", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "courtName", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "gameId", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "gamePortrait", "0", base)
                json_package(rep["returndata"]["topicData"][r_count]["matchInfo"], "matchId", "0", base)
            else:

                json_package(rep["returndata"]["topicData"][r_count], "Comment", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "targetName", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "userName", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "publish_time", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "browserNumber", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "targetPortrait", "0", base)
                json_package(rep["returndata"]["topicData"][r_count], "matchId", "0", base)
                if "matchList" in rep["returndata"]["topicData"][r_count]["dataInfo"]:
                    print("=======学校======")
                    matchList_count = int(len(rep["returndata"]["topicData"][r_count]["dataInfo"]["matchList"]))
                    for m_count in range(matchList_count):
                        json_package(rep["returndata"]["topicData"][r_count]["dataInfo"]["matchList"][m_count],
                                     "courtName",
                                     "0", base)
                        json_package(rep["returndata"]["topicData"][r_count]["dataInfo"]["matchList"][m_count],
                                     "turnsName",
                                     "0", base)
                        json_package(rep["returndata"]["topicData"][r_count]["dataInfo"]["matchList"][m_count],
                                     "gameName",
                                     "0", base)
                        json_package(rep["returndata"]["topicData"][r_count]["dataInfo"]["matchList"][m_count],
                                     "gameId",
                                     "0", base)
                        json_package(rep["returndata"]["topicData"][r_count]["dataInfo"]["matchList"][m_count],
                                     "gamePortrait", "0", base)
                        json_package(rep["returndata"]["topicData"][r_count]["dataInfo"]["matchList"][m_count],
                                     "matchId", "0", base)
                else:
                    continue
            url = "/lyc/save_dongtai"
            data = base
            response_api(url, data)
            # print("json:", str(base).replace("'", '"'))
            # print("")


if __name__ == '__main__':
    dynamic()
