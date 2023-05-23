from tools.requests_get import requests_get
from tools.json_data_handle import json_data_handle_single
from tools.response_api import response_api


def scoreboard_data(teamId):
    print("数据:")
    url = "https://sportdatax.suning.com/sdfocus-web/client/playersAndTeam/getTeamData.do?_source=ppsports&apptype=android&appversion=5.29&teamId=" + teamId + "&clientType=1 "
    result = requests_get(url)
    # print(result)
    data_dict = {}
    data_dict["teamId"] = teamId
    data = result["data"]
    base_url = "https://sportdatax.suning.com/sdfocus-web/client/playersAndTeam/getTeamDetail.do?_source=ppsports&apptype=android&appversion=5.29&iversion=1.0&appversion=5.29&apptype=Android&teamId=" + teamId + "&appid=PPTVSPORTSNO1&appplt=aph&appver=5.29&ppi=AgACAAAABwAATkwAAAAHAAAAAGAUMQA5a9BIU6p32kjbMU3vCy_SGOj77OG9lx0kB5LXwUtldQNnCzx-rV1qNHJgAfUc4EpqHDYJrp3KUex6UcX-j1kd"
    base_text = requests_get(base_url)
    base_list = ["address", "codeTeam", "countryLogo", "countryName", "email", "fansCount", "marketValue", "setupTime",
                 "teamEnName", "teamId", "teamLogo", "teamName", "teamShortName", "telephone", "venueCapacity",
                 "venueName", "worldRank"]

    base_dict = json_data_handle_single(base_text["data"], base_list)
    data_dict["baseInfo"] = base_dict
    data_dict["data"] = data
    # print(base_dict)
    response_api("/sszqbf/save_qiuduixiangxi_shuju", data_dict)
    # print(data_dict)


if __name__ == '__main__':
    # 263
    scoreboard_data(str(263))
