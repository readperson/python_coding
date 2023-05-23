from tools.requests_get import requests_get
from tools.json_data_handle import json_data_handle_single
from tools.response_api import response_api


def scoreborad_information(teamId):
    print("资讯列表：")
    url = "https://sportdatax.suning.com/sdfocus-web/client/playersAndTeam/getTeamNewsList.do?_source=ppsports&apptype=android&appversion=5.29&pageNum=1&apptype=android&teamId=" + teamId + "&iversion=1.0&appversion=5.29"
    text = requests_get(url)
    infor_dict = {}
    infor_dict["teamId"] = teamId
    infor_dict["data"] = text["data"]
    # print(infor_dict)
    response_api("/sszqbf/save_qiuduixiangxi_zixunliebiao", infor_dict)
    # 资讯详细
    print("资讯详细")
    contentList_count = int(len(infor_dict["data"]["contentList"]))
    for cl_c in range(contentList_count):
        if cl_c > 15:
            break
        detailed_dict = {}
        contentId = str(infor_dict["data"]["contentList"][cl_c]["contentId"])
        detailed_dict["teamId"] = teamId
        detailed_dict["contentId"] = contentId
        url_detailed = "https://snsis.suning.com/snsis-web/client/queryContentDetails/" + contentId + "/1/android/5.29/1.2.htm?_source=ppsports&apptype=android&appversion=5.29&iversion=1.2&_source=ppsports&apptype=android&appversion=5.29"
        detailed_text = requests_get(url_detailed)
        detailed_list = ["commentNum", "content=base64", "contentId", "contentType", "cover", "createTime", "headPic",
                         "likeNum",
                         "nickName", "authorId", "nowTime", "title", "authorType", "authentInfo", "vFlag",
                         "sourceDetailType",
                         "subjectId", "subjectName", "subjectType", "matchIds", "sourceType", "contentTag",
                         "contentTag",
                         "advSource", "authorFlag", "authorFlagDesc", "themeId"]
        detailed_dict["data"] = json_data_handle_single(detailed_text["data"]["contentBean"], detailed_list)
        # print(detailed_dict)

        response_api("/sszqbf/save_qiuduixiangxi_zixunxiangxi", detailed_dict)


if __name__ == '__main__':
    scoreborad_information("263")
