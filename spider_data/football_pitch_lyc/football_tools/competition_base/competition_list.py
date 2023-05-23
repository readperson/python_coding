import sys

sys.path.append("/opt/data_captureAPP")
from tools.headers_json.headers_json import headers_json
from tools.requests_api import requests_api
from football_pitch_lyc.football_tools.competition_detailed.competition_list import competition_list
import math
from tools.response_api import response_api


# gameStatus 进行中 10 ,已结束 30  "gameNum": "286"
def lyc_competion():
    gamestatus_list = [10, 30]
    gamestatus_count = int(len(gamestatus_list))
    for g_count in range(gamestatus_count):
        gamestatus = gamestatus_list[g_count]
        # 比赛列表 总页数
        url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
        data = 'json={"uid":5481238,"method":"game_common_getGameList","gameStatus":' + str(
            gamestatus) + ',"areaId":"22","condition":"","page":1,"limit":10,"sportType":"1","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"1f37caeda1c7109ef006082fb93f47d8f9e90e6c"}'
        headers = headers_json()
        rep = requests_api(url=url, headers=headers, data=data)
        # gameNum = math.ceil(int(rep["returndata"]["gameNum"]) / 10)
        gameNum = 1
        # print("gameNum", gameNum)
        page = 1
        for p in range(gameNum):
            # 比赛列表  gameStatus  page
            url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
            data = 'json={"uid":5481238,"method":"game_common_getGameList","gameStatus":' + str(
                gamestatus) + ',"areaId":"22","condition":"","page":' + str(
                page) + ',"limit":10,"sportType":"1","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"1f37caeda1c7109ef006082fb93f47d8f9e90e6c"}'
            rep = requests_api(url=url, headers=headers, data=data)
            rep_count = int(len(rep["returndata"]["gameList"]))

            # print(rep)
            for r_c in range(rep_count):
                print("gamestatus", gamestatus, "共有", gameNum, "页,正在处理第", page, "页的第", r_c + 1, "条数据")
                base = {}
                base["game_status"] = str(gamestatus)
                base = competition_list(rep["returndata"]["gameList"][r_c], base)
                base["gamename"] = str(base["gamename"]).replace("彩票", "")
                # print("json:", str(base).replace("'", '"'))
                # print("")
                #     /lyc/save_saishi_liebiao
                url = "/lyc/save_saishi_liebiao"
                response_api(url, base)

            page = page + 1


if __name__ == '__main__':
    lyc_competion()
