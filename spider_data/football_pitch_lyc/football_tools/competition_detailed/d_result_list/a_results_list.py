import sys

sys.path.append("/opt/data_captureAPP")
from football_pitch_lyc.football_tools.competition_detailed.d_result_list.player_accumulate_points import \
    player_accumulate_points
from football_pitch_lyc.football_tools.competition_detailed.d_result_list.discipline_list import discipline_list
from football_pitch_lyc.football_tools.competition_detailed.d_result_list.scoreboard import scoreboard
from football_pitch_lyc.football_tools.competition_detailed.d_result_list.shooter_list import shooter_list
from football_pitch_lyc.football_tools.competition_detailed.d_result_list.hot_ballGame_Player import hot_ballGame
from football_pitch_lyc.football_tools.competition_detailed.headers_json import headers_json
from tools.ID_file.gameid_return_list import gameid_return_list
from tools.response_api import response_api


def results_list(gameId):
    # 榜单 results_list  gameId
    # 榜单 热度榜 hot_ball_game player
    headers = headers_json()
    results_dict = {}
    results_dict["gameId"] = gameId
    hot = hot_ballGame(gameId, headers)
    results_dict["hot"] = hot

    # 榜单 积分榜 gameId
    scoreboard_dcit = {}
    # score = scoreboard(gameId, headers)
    # print(gameId)
    scoreboard_list = scoreboard(gameId, headers)
    results_dict["scoreboard_list"] = scoreboard_list

    # 榜单 球员
    # 射手 gameId
    # https://online.greenplayer.cn/E901D2019YBT/api/game/loadGameScoreRankList.php
    # json={"gameId":"33426","rankType":1,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"81f4862645b5ca0d9568c62c87f469fa8e23c80e"}
    player_list = {}
    shooter_data = 'json={"gameId":"' + gameId + '","rankType":1,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"81f4862645b5ca0d9568c62c87f469fa8e23c80e"}'
    shooter = shooter_list(headers, shooter_data)
    player_list["shooter"] = shooter

    # 助攻  gameId holding_attack
    # json={"gameId":"33426","rankType":3,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"f854174045ba71a3fbc4b53c586ba4c2b9e508ea"}
    holding_attack_data = 'json={"gameId":"' + gameId + '","rankType":3,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"f854174045ba71a3fbc4b53c586ba4c2b9e508ea"}'
    holding_attack = shooter_list(headers, holding_attack_data)
    player_list["holding_attack"] = holding_attack

    # 纪律 gameId  discipline
    # https://online.greenplayer.cn/E901D2019YBT/api/game/loadGamePunishRankList.php
    # json={"gameId":"33426","orderType":"1","version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"061d5798459f7dab2937971d1172c8689a817f79"}
    data = 'json={"gameId":"' + gameId + '","orderType":"1","version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"061d5798459f7dab2937971d1172c8689a817f79"}'

    discipline = discipline_list(headers, data)
    player_list["discipline"] = discipline

    #  gameId 球员积分
    # json={"method":"match_player_getGameMatchPlayerListByTeamId","uid":5481238,"gameId":"33426","teamId":"","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"3bb0892eed713e4ab64776556c29fba22182db50"}
    data = 'json={"method":"match_player_getGameMatchPlayerListByTeamId","uid":5481238,"gameId":"' + gameId + '","teamId":"","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"3bb0892eed713e4ab64776556c29fba22182db50"}'
    accumulate_points = player_accumulate_points(headers, data)
    player_list["player_accumulate_points"] = accumulate_points

    results_dict["player_list"] = player_list
    # /lyc/save_bangdan
    url = "/lyc/save_bangdan"
    response_api(url, results_dict)

    # print("json",results_dict)


if __name__ == '__main__':
    gameID_list = gameid_return_list()
    gameid_count = int(len(gameID_list))
    for g_count in range(gameid_count):
        print("共有球队数据", gameid_count, "条，正在处理第", g_count + 1, "条数据")
        results_list(gameID_list[g_count])
        # results_list(str(34562))
