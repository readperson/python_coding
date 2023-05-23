from tools.requests_get import requests_get
from tools.response_api import response_api


def scoreboard_schedule(teamId):
    print("赛程：")
    url = "https://sportdatax.suning.com/sdfocus-web/client/team/getTeamSchedule.do?_source=ppsports&apptype=android&appversion=5.29&teamId=" + teamId
    result = requests_get(url)
    schedule_dict = {}
    schedule_dict["teamId"] = teamId
    schedule_dict["data"] = result["data"]
    # print(schedule_dict)
    response_api("/sszqbf/save_qiuduixiangxi_saicheng", schedule_dict)


if __name__ == '__main__':
    scoreboard_schedule(str(263))
