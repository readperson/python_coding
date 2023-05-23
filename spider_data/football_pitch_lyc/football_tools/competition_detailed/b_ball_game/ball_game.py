import sys

sys.path.append("/opt/data_captureAPP")
from football_pitch_lyc.football_tools.competition_detailed.headers_json import headers_json
from tools.requests_api import requests_api
from football_pitch_lyc.football_tools.competition_detailed.b_ball_game.ball_game_list import ball_game_lists
from football_pitch_lyc.football_tools.competition_detailed.b_ball_game.view_entry_Information import \
    view_entry_Information
from tools.ID_file.gameid_return_list import gameid_return_list
from tools.response_api import response_api


def ball_game(gameId):
    headers = headers_json()
    ball_game_base = {}
    ball_game_base["gameId"] = gameId

    ball_game_url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
    ball_game_data = 'json={"method":"game_team_getGameTeamList","gameId":"' + str(
        gameId) + '","version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"57781c2b4ed4db3fccf5f18bffc144741435ed9a"}'
    ball_game_rep = requests_api(url=ball_game_url, headers=headers, data=ball_game_data)
    # print("ball_game_rep", ball_game_rep)
    ball_game_count = int(len(ball_game_rep["returndata"]["teamList"]))

    ball_game_list = []
    for bg_count in range(ball_game_count):
        ball_game_dict = ball_game_lists(ball_game_rep["returndata"]["teamList"][bg_count])
        teamId = ball_game_dict["teamId"]
        view_entry_Info = view_entry_Information(gameId, teamId, headers)
        ball_game_dict["view_entry_Info"] = view_entry_Info
        ball_game_list.append(ball_game_dict)
    ball_game_base["data"] = ball_game_list
    print(ball_game_base)
    url = "/lyc/save_saishi_qiudui"
    response_api(url, ball_game_base)


if __name__ == '__main__':
    gameID_list = gameid_return_list()
    gameid_count = int(len(gameID_list))
    for g_count in range(gameid_count):
        print("共有球队数据", gameid_count, "条，正在处理,第", g_count + 1, "条数据")
        ball_game(gameID_list[g_count])
