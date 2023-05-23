from tools.requests_get import requests_get
import json
from tools.response_api import response_api

def scoreboard_TeamPlayer(teamId):
    print("球员")
    team_player = {}
    team_player["teamId"] = teamId
    url = "https://sportdatax.suning.com/sdfocus-web/client/playersAndTeam/getTeamPlayerVerticalScreen.do?_source=ppsports&apptype=android&appversion=5.29&sort=1&teamId=" + teamId
    result = requests_get(url)
    result = json.loads(str(result).replace("None", "''").replace("'", '"'))
    team_player["data"] = result["data"]

    # print(team_player)
    response_api("/sszqbf/save_qiuduixiangxi_qiuyuan",team_player)

if __name__ == '__main__':
    scoreboard_TeamPlayer(str(1216))
