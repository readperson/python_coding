import sys

sys.path.append("/opt/data_captureAPP")
from tools.headers_json.headers_json import headers_json
import requests
import json
from tools.ID_file.matchid_return_list import matchid_return_list
from football_pitch_lyc.football_tools.competition_Details_team.isterinfo import isterinfo
from tools.json_package.json_package import json_package
from tools.response_api import response_api

# 名单 matchId
def name_list(matchId):
    url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
    registerInfo = {}
    registerInfo["matchId"] = matchId
    headers = headers_json()
    data = 'json={"method":"match_match_getMatchTeamPlayerShowUpList","uid":5481238,"matchId":"' + matchId + '","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"d585fb849a90d7d0d3c0a76fe94423f4c661e430"}'
    response_name_list = requests.post(url=url, headers=headers, data=data)
    response_name_list.encoding = "utf-8"
    response_name_list = json.loads(response_name_list.text.replace("﻿", ""))
    # print("-----------response_name_list", response_name_list)
    # "party_a": "10272",
    # "party_b": "50955",
    # "activityIdA": "517511",
    # "activityIdB": "517512",
    json_package(response_name_list["returndata"], "party_a", "", registerInfo)
    json_package(response_name_list["returndata"], "party_b", "", registerInfo)
    json_package(response_name_list["returndata"], "activityIdA", "", registerInfo)
    json_package(response_name_list["returndata"], "activityIdB", "", registerInfo)
    registerInfo_a = response_name_list["returndata"]["registerInfo_a"]
    registerInfo["registerInfo_a"] = isterinfo(registerInfo_a)
    registerInfo_b = response_name_list["returndata"]["registerInfo_b"]
    registerInfo["registerInfo_b"] = isterinfo(registerInfo_b)
    unRegisterInfo_a = response_name_list["returndata"]["unRegisterInfo_a"]
    registerInfo["unRegisterInfo_a"] = isterinfo(unRegisterInfo_a)
    unRegisterInfo_b = response_name_list["returndata"]["unRegisterInfo_b"]
    registerInfo["unRegisterInfo_b"] = isterinfo(unRegisterInfo_b)
    # print(registerInfo)
    url ="/lyc/save_mingdan"
    data =registerInfo
    response_api(url,data)



if __name__ == '__main__':
    matchId_list = matchid_return_list()
    # print(int(len(matchId_list)))
    for m_index in range(int(len(matchId_list))):
        print("共有名单数据：", int(len(matchId_list)), "条", "正在处理", m_index + 1, "条")
        matchId = matchId_list[m_index]
        # print(matchId)
        te = name_list(matchId)
        # print(te)
