import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
import math
from tools.base64_text import text_conversion_base64
from tools.response_api import response_api
from tools.time_treatment import now_time


# 一起浪电竞 训练比赛 品牌赛事
def brand_competition_list():
    url_page_count = "https://yql-service.e7lang.com/api/app/brand?showToast=function+(t)%7Bs.showToastWithIcon(t)%7D&game=HPJY&" \
                     "page=1&size=10&successData=function+(t)%7Bvar+o%3Dn.props,s%3Do.pageSize,l%3Do.setCurrentData%3Bn.setState" \
                     "(%7BcurrentData:t,haveInit:!0%7D),1%3D%3D%3Dn.page%3F(n.state.isNoMoreData%3Dt.length%3Cs,n.setState" \
                     "(%7Bdata:t,refreshing:!1,isNoMoreData:t.length%3Cs%7D),l%26%26l(t)):(n.state.isNoMoreData%3Dt.length%3Cs,n." \
                     "loadMoreing%3D!1,n.setState(%7Bdata:n.state.data.concat(t),isNoMoreData:t.length%3Cs,loadMoreing:!1," \
                     "refreshing:!1%7D),l%26%26l(n.state.data.concat(t)))%7D"
    brand_competition_page_count = json.loads(requests.get(url=url_page_count).text)
    total = brand_competition_page_count["total"]
    i = math.ceil(total / 10)
    for page in range(i):
        page = page + 1
        url = "https://yql-service.e7lang.com/api/app/brand?showToast=function+(t)%7Bs.showToastWithIcon(t)%7D&game=HPJY&" \
              "page=" + str(
            page) + "&size=10&successData=function+(t)%7Bvar+o%3Dn.props,s%3Do.pageSize,l%3Do.setCurrentData%3Bn.setState" \
                    "(%7BcurrentData:t,haveInit:!0%7D),1%3D%3D%3Dn.page%3F(n.state.isNoMoreData%3Dt.length%3Cs,n.setState" \
                    "(%7Bdata:t,refreshing:!1,isNoMoreData:t.length%3Cs%7D),l%26%26l(t)):(n.state.isNoMoreData%3Dt.length%3Cs,n." \
                    "loadMoreing%3D!1,n.setState(%7Bdata:n.state.data.concat(t),isNoMoreData:t.length%3Cs,loadMoreing:!1," \
                    "refreshing:!1%7D),l%26%26l(n.state.data.concat(t)))%7D"
        brand_competition = json.loads(requests.get(url=url).text)
        brand_competition_count = int(len(brand_competition["data"]))
        for bc_count in range(brand_competition_count):
            print("训练比赛,品牌赛事共有", i, "页,正在处理第", page, "页的第", bc_count + 1, "条数据", "处理时间:", now_time())
            brand_competition_dict = {}
            id = brand_competition["data"][bc_count]["id"]
            name = brand_competition["data"][bc_count]["name"]
            game = brand_competition["data"][bc_count]["game"]
            logo = brand_competition["data"][bc_count]["logo"]
            trainingLogo = brand_competition["data"][bc_count]["trainingLogo"]
            randIndex = brand_competition["data"][bc_count]["randIndex"]
            memberNumber = brand_competition["data"][bc_count]["memberNumber"]
            introduction = brand_competition["data"][bc_count]["introduction"]
            introduction = text_conversion_base64(introduction)
            createTime = brand_competition["data"][bc_count]["createTime"]
            brand_competition_dict["id"] = id
            brand_competition_dict["name"] = name
            brand_competition_dict["game"] = game
            brand_competition_dict["logo"] = logo
            brand_competition_dict["trainingLogo"] = trainingLogo
            brand_competition_dict["randIndex"] = randIndex
            brand_competition_dict["memberNumber"] = memberNumber
            brand_competition_dict["createTime"] = createTime
            brand_competition_dict["introduction"] = introduction

            url_club = "/esports/save_esports_brand_match"
            response_api(url_club, brand_competition_dict)


if __name__ == '__main__':
    brand_competition_list()
