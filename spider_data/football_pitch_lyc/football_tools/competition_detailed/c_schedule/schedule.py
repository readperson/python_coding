import sys

sys.path.append("/opt/data_captureAPP")
from football_pitch_lyc.football_tools.competition_detailed.headers_json import headers_json
from tools.requests_api import requests_api
from tools.ID_file.gameid_return_list import gameid_return_list
from football_pitch_lyc.football_tools.competition_detailed.c_schedule.schedule_list import schedule_list
from tools.response_api import response_api


def schedule(gameId):
    schedule = {}
    schedule["gameId"] = gameId
    headers = headers_json()
    schedule_url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
    schedule_data = 'json={"uid":"5481238","method":"game_common_getGameScheduleMatchListNew","gameId":"' + str(
        gameId) + '","currentTurn":"","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"e4e50212571c1ac98925460598622e761f83fce6"}'
    info_schedule = requests_api(url=schedule_url, headers=headers, data=schedule_data)
    # print("info_schedule", info_schedule)
    if "returndata" in info_schedule:
        matchList_count = int(len(info_schedule["returndata"]["matchList"]))
    else:
        print("")
    # print("matchList_count", matchList_count)
    matchList = []
    for m_count in range(matchList_count):
        matchDict = schedule_list(info_schedule["returndata"]["matchList"][m_count])
        matchDict["paly_order"] = str(m_count + 1)
        matchList.append(matchDict)
    schedule["data"] = matchList
    url = "/lyc/save_saishi_saicheng"
    response_api(url, schedule)
    # print(schedule)


if __name__ == '__main__':
    gameID_list = gameid_return_list()
    gameid_count = int(len(gameID_list))
    for g_count in range(gameid_count):
        print("共有赛程数据", gameid_count, "条，正在处理第", g_count + 1, "条数据")
        schedule(gameID_list[g_count])
        # schedule(33426)
