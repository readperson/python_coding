import sys

sys.path.append("/opt/data_captureAPP")
from tools.headers_json.headers_json import headers_json
import requests
import json
from tools.json_package.json_package import json_package
from tools.ID_file.Teamid_return_list import teamid_return_list
import time
from tools.response_api import response_api


# 预测 teamId
def forecast(teamId):
    url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
    data = 'json={"method":"team_match_getTeamDataInfo","uid":5481238,"teamId":"' + teamId + '","page":1,"numberPage":5,"version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"af3bb816b2c2c5cbe1c0a90ab40972072a4b2058"}'
    headers = headers_json()

    time.sleep(1)
    reponse_forecast = requests.post(url=url, headers=headers, data=data)
    print(reponse_forecast.text)
    reponse_forecast.encoding = "utf-8"
    reponse_forecast = json.loads(reponse_forecast.text)
    reponse_forecast_count = int(len(reponse_forecast["returndata"]["matchData"]))
    forecast_list = []
    forecast = {}
    forecast["teamId"] = teamId

    index = 0
    for rf_count in range(reponse_forecast_count):
        forecast_dict = {}
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "matchResult", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "court_id", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "court_number_id", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "homeTeamId", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "awayTeamId", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "homeName", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "awayName", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "awayIcon", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "awayName", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "homeScore", "", forecast_dict)
        json_package(reponse_forecast["returndata"]["matchData"][rf_count], "awayScore", "", forecast_dict)
        index = index + 1
        forecast_list.append(forecast_dict)
    forecast["forecast"] = forecast_list
    # print(forecast)
    url = "/lyc/save_yuce"
    data = forecast
    response_api(url, data)


if __name__ == '__main__':
    teamid_list = teamid_return_list()
    teamid_list_count = int(len(teamid_list))
    print(teamid_list_count)
    # D:\pythonworkspace\data_captureAPP\football_pitch_lyc\football_tools\competition_Details_team
    # football_pitch_lyc/football_tools/competition_Details_team
    index_failed = "index_failed.txt"
    # index_failed = "/opt/data_captureAPP/football_pitch_lyc/football_tools/competition_Details_team/index_failed.txt"
    index = 0
    with open(index_failed, "r", encoding="utf-8") as f:
        index_file = int(f.read())
        if index_file != 0:
            print("----------------")
            index = index_file
            with open(index_failed, "w", encoding="utf-8") as f1:
                f1.write("0")
    teamid_list_count = teamid_list_count - int(index)

    try:
        for tl_count in range(teamid_list_count):
            print("index:", index)
            teamid = teamid_list[index]
            print("共有预测数据：", len(teamid_list), "条", "正在处理", index + 1, "条", teamid)
            # print(type(teamid))
            if int(teamid) == 0:
                index = index + 1
                continue
            forecast(teamid)
            index = index + 1
    except Exception  as e:
        with open(index_failed, "w", encoding="utf-8") as f1:
            string = (str(index))
            f1.write(string)
        print("=====================================异常==========================================")
        print(e)
