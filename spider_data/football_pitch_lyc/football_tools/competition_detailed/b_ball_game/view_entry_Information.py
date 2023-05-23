import requests
import json
from tools.requests_api import requests_api
from tools.json_package.json_package import json_package

# 球队查看详细
def view_entry_Information(gameId, teamId, headers):
    view_info = {}
    url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
    data = 'json={"method":"game_team_getTeamGameInfo","gameId":"' + str(gameId) + '","teamId":"' + teamId + '","dataType":4,"loadType":2,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"95ae74080aca18bcbd7a6b33e71bee8320995b8c"}'
    rep = requests_api(url=url, headers=headers, data=data)
    json_package(rep["returndata"]["gameInfo"], "startTime", "", view_info)
    json_package(rep["returndata"]["gameInfo"], "portrait", "", view_info)
    json_package(rep["returndata"]["gameInfo"], "gameName", "", view_info)
    json_package(rep["returndata"]["gameInfo"], "teamnumber", "", view_info)
    json_package(rep["returndata"]["gameInfo"], "statusName", "", view_info)
    json_package(rep["returndata"]["gameInfo"], "gameTitle", "", view_info)
    json_package(rep["returndata"]["teamInfo"], "teamId", "", view_info)
    json_package(rep["returndata"]["teamInfo"], "teamName", "", view_info)
    json_package(rep["returndata"]["teamInfo"], "portrait", "", view_info)
    json_package(rep["returndata"]["gameInfo"], "coachId", "", view_info)
    json_package(rep["returndata"]["gameInfo"], "coachName", "", view_info)
    json_package(rep["returndata"]["gameInfo"], "coachPortrait", "", view_info)
    playerList_count = int(len(rep["returndata"]["playerList"]))
    # print("playerList_count", playerList_count)
    player_List = []
    for p_count in range(playerList_count):
        player_Dict = {}
        json_package(rep["returndata"]["playerList"][p_count], "playerId", "", player_Dict)
        json_package(rep["returndata"]["playerList"][p_count], "str1", "", player_Dict)
        json_package(rep["returndata"]["playerList"][p_count], "playerPortrait", "", player_Dict)
        json_package(rep["returndata"]["playerList"][p_count], "playerName", "", player_Dict)
        json_package(rep["returndata"]["playerList"][p_count], "playerNumber", "", player_Dict)
        json_package(rep["returndata"]["playerList"][p_count], "position", "", player_Dict)
        player_Dict["playerPortrait"] = ""
        player_List.append(player_Dict)
    view_info["playerList"] = player_List
    return view_info
