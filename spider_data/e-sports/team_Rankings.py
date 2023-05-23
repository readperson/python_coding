import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
import math
from tools.json_package_upgrade_version import json_package
from tools.base64_text import text_conversion_base64
from tools.response_api import response_api
from tools.time_treatment import now_time


# 一起浪电竞 战队排行榜
def team_rankings():
    url = "https://yql-service.e7lang.com/api/app/teams?showToast=function+(t)%7Bs.showToastWithIcon(t)%7D&game=HPJY&page=1&size=10&successData=function+(t)%7Bvar+o%3Dn.props,s%3Do.pageSize,l%3Do.setCurrentData%3Bn.setState(%7BcurrentData:t,haveInit:!0%7D),1%3D%3D%3Dn.page%3F(n.state.isNoMoreData%3Dt.length%3Cs,n.setState(%7Bdata:t,refreshing:!1,isNoMoreData:t.length%3Cs%7D),l%26%26l(t)):(n.state.isNoMoreData%3Dt.length%3Cs,n.loadMoreing%3D!1,n.setState(%7Bdata:n.state.data.concat(t),isNoMoreData:t.length%3Cs,loadMoreing:!1,refreshing:!1%7D),l%26%26l(n.state.data.concat(t)))%7D"
    team_rankings_list = requests.get(url=url)
    team_rankings_list = json.loads(team_rankings_list.text)
    total_count = team_rankings_list['total']
    pageCount = math.ceil(total_count / 10)
    print(pageCount)
    if pageCount > 5:
        pageCount = 5
    for page in range(pageCount):
        page += 1
        url_page = "https://yql-service.e7lang.com/api/app/teams?showToast=function+(t)%7Bs.showToastWithIcon(t)%7D&game=HPJY&page=" + str(
            page) + "&size=10&successData=function+(t)%7Bvar+o%3Dn.props,s%3Do.pageSize,l%3Do.setCurrentData%3Bn.setState(%7BcurrentData:t,haveInit:!0%7D),1%3D%3D%3Dn.page%3F(n.state.isNoMoreData%3Dt.length%3Cs,n.setState(%7Bdata:t,refreshing:!1,isNoMoreData:t.length%3Cs%7D),l%26%26l(t)):(n.state.isNoMoreData%3Dt.length%3Cs,n.loadMoreing%3D!1,n.setState(%7Bdata:n.state.data.concat(t),isNoMoreData:t.length%3Cs,loadMoreing:!1,refreshing:!1%7D),l%26%26l(n.state.data.concat(t)))%7D"
        team_rankings_list_page = requests.get(url=url_page)
        team_rankings_list_page = json.loads(team_rankings_list_page.text)
        data_count = int(len(team_rankings_list_page['data']))
        for da_count in range(data_count):
            team_rankings_list_dict = {}
            print("战队排行榜共有", pageCount, "页,正在处理第", page, "页的第", da_count + 1, "条数据", "处理时间:", now_time())
            json_package(team_rankings_list_page['data'][da_count], "ranking", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "id", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "showId", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "blackLogo", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "name", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "declaration", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "clubId", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "clubName", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "businessValue", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "game", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "createTime", "", team_rankings_list_dict)
            json_package(team_rankings_list_page['data'][da_count], "updateTime", "", team_rankings_list_dict)
            url_team_rankings_list_dict = "/esports/save_esports_paihangbang_zhandui"
            response_api(url_team_rankings_list_dict, team_rankings_list_dict)
            print("战队列表数据", team_rankings_list_dict)

            url_team_information = "https://yql-service.e7lang.com/api/app/training/" + str(
                team_rankings_list_dict["showId"]) + "/info"
            headers = {"Host": "yql-service.e7lang.com"}
            team_information = requests.get(url=url_team_information, headers=headers)
            print("team_information", team_information.text)
            team_information = json.loads(team_information.text)
            team_information_count = int(len(team_information))
            for t_icount in range(team_information_count):
                team_information_dict = {}
                team_information_dict["pkey"] = team_rankings_list_dict["pkey"]
                team_information_dict["showId"] = team_rankings_list_dict["showId"]
                json_package(team_information[t_icount], "brandId", "", team_information_dict)
                json_package(team_information[t_icount], "brandName", "",
                             team_information_dict)
                json_package(team_information[t_icount], "totalGameNums", "",
                             team_information_dict)
                json_package(team_information[t_icount], "chickens", "",
                             team_information_dict)
                json_package(team_information[t_icount], "totalGameKills", "",
                             team_information_dict)
                json_package(team_information[t_icount], "totalIntegral", "",
                             team_information_dict)
                url_team_information_dict = "/esports/save_esports_paihangbang_zhanduixinxi"
                response_api(url_team_information_dict, team_information_dict)
                print("参赛信息：", team_information_dict)

            url_team_members = "https://yql-service.e7lang.com/api/app/teams/" + str(
                team_rankings_list_dict['pkey']) + "/members?page=1&size=10"
            team_members = requests.get(url=url_team_members)
            team_members = json.loads(team_members.text)
            team_members_pageCount = math.ceil(int(team_members["total"]) / 10)
            if team_members_pageCount > 5:
                team_members_pageCount = 5
            for t_m_page in range(team_members_pageCount):
                url_team_members_page = "https://yql-service.e7lang.com/api/app/teams/" + str(
                    team_rankings_list_dict['pkey']) + "/members?page=" + str(t_m_page + 1) + "&size=10"
                team_members_page = requests.get(url=url_team_members_page)
                team_members_page = json.loads(team_members_page.text)
                data_count_page = int(len(team_members_page["data"]))
                for d_c_page in range(data_count_page):
                    team_members_dict = {}
                    team_members_dict['pkey'] = team_rankings_list_dict["pkey"]
                    team_members_dict['showId'] = team_rankings_list_dict["showId"]
                    json_package(team_members_page["data"][d_c_page], "teamMemberId", "", team_members_dict)
                    json_package(team_members_page["data"][d_c_page], "teamId", "", team_members_dict)
                    json_package(team_members_page["data"][d_c_page], "gamerId", "", team_members_dict)
                    json_package(team_members_page["data"][d_c_page], "gamerName", "", team_members_dict)
                    team_members_dict['gamerName'] = text_conversion_base64(
                        team_members_page["data"][d_c_page]["gamerName"])
                    json_package(team_members_page["data"][d_c_page], "teamName", "", team_members_dict)
                    json_package(team_members_page["data"][d_c_page], "gamerLogo", "", team_members_dict)
                    json_package(team_members_page["data"][d_c_page], "showGamerId", "", team_members_dict)
                    json_package(team_members_page["data"][d_c_page], "jobType", "", team_members_dict)
                    url_value = "https://yql-service.e7lang.com/api/app/users/valuation?userId=" + str(
                        team_members_dict["gamerId"]) + "&game=HPJY"
                    team_value = requests.get(url=url_value)
                    team_value = json.loads(team_value.text)
                    team_members_dict["totalValue"] = str(team_value["totalValue"])
                    url_team_members_dict = "/esports/save_esports_paihangbang_zhanduichengyuan"
                    response_api(url_team_members_dict, team_members_dict)
                    print("战队成员", team_members_dict)

            print(team_members_pageCount)
            print("")


if __name__ == '__main__':
    team_rankings()
