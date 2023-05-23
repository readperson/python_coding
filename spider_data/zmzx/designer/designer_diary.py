import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.json_package import json_package
from zmzx.tools.response_api import response_api
import math
from tools.base64_text import text_conversion_base64
from zmzx.tools.comment import comment
from zmzx.tools.request_api import request_api


# 日记
def designer_diary(user_id):
    url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/whd/someone/search"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"page_size": 10, "owner_id": str(user_id), "user_id": "", "page_index": 0}
    diary_list = response_api(url, headers, data)
    # print(diary_list)
    total_records = diary_list["total_records"]
    pageCount = math.ceil(total_records / 10)
    if pageCount > 3:
        pageCount = 3
    for page in range(pageCount):
        data_page = {"page_size": 10, "owner_id": str(user_id), "user_id": "", "page_index": str(page)}
        diary_list_page = response_api(url, headers, data_page)
        # records
        # print("日记列表原始数据：", diary_list_page)
        records_count = int(len(diary_list_page["records"]))
        for r_count in range(records_count):
            print("共有日记", total_records, "条,", pageCount, "页", "正在处理第", page + 1, "页,第", r_count + 1, "条数据")
            diary_list_dict = {}
            json_package(diary_list_page["records"][r_count], "diary_id", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "title", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "cover_url", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "user_id", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "nickname", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "avatar", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "house_type", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "area", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "style", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "budget", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "id", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "vote_count", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "collect_count", "", diary_list_dict)
            json_package(diary_list_page["records"][r_count], "comment_count", "", diary_list_dict)
            request_api("/zmzx/save_shejishi_riji", diary_list_dict)
            # print("日记列表：", diary_list_dict)

            # 日记详细
            diary_detailed_url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/live-diary/detail"
            diary_detailed_data = {"id": str(diary_list_dict["diary_id"]), "return_comment_count": 3}
            diary_detailed_result = response_api(diary_detailed_url, headers, diary_detailed_data)
            # print("日记详细原始数据：", diary_detailed_result)
            diary_detailed_dict = {}
            json_package(diary_detailed_result["live_diary"], "id", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "title", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "cover_url", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "user_id", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "nickname", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "avatar", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "house_type", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "area", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "budget", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "style", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "city", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "show_home_count", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "fans_count", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "collect_count", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "share_count", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "vote_count", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "comment_count", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "reservation_count", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "designer_city", "", diary_detailed_dict)
            json_package(diary_detailed_result["live_diary"], "page_view", "", diary_detailed_dict)
            # create_time
            diary_detailed_dict["create_time"] = str(diary_detailed_result["live_diary"]["create_time"]).replace("T",
                                                                                                                 " ")
            # comment_list
            if "comment_list" in diary_detailed_result["live_diary"]:
                comment_list_count = int(len(diary_detailed_result["live_diary"]["comment_list"]))
                for clist_count in range(comment_list_count):
                    comment_dict = comment(diary_detailed_result["live_diary"]["comment_list"][clist_count],
                                           "diary_id", diary_list_dict["diary_id"])
                    photo_url_count = int(len(comment_dict["sender_photo_url"]))
                    comment_dict["data_pkey"] = diary_list_dict["diary_id"]
                    comment_dict["type"] = "1000200"
                    if photo_url_count == 0:
                        print("评论头像为空 放弃！")
                        continue
                    # print("日记评论:", comment_dict)
                    request_api("/zmzx/save_ext_pinglun", comment_dict)

            info_list_count = int(len(diary_detailed_result["live_diary"]["live_diary_info_list"]))
            live_diary_info_list = []
            for i_list_count in range(info_list_count):
                live_diary_info_dict = {}
                json_package(diary_detailed_result["live_diary"]["live_diary_info_list"][i_list_count], "id", "",
                             live_diary_info_dict)
                live_diary_info_dict["content"] = text_conversion_base64(
                    diary_detailed_result["live_diary"]["live_diary_info_list"][i_list_count]["content"])
                json_package(diary_detailed_result["live_diary"]["live_diary_info_list"][i_list_count], "pic_url", "",
                             live_diary_info_dict)
                json_package(diary_detailed_result["live_diary"]["live_diary_info_list"][i_list_count], "label_names",
                             "", live_diary_info_dict)
                json_package(diary_detailed_result["live_diary"]["live_diary_info_list"][i_list_count], "img_width", "",
                             live_diary_info_dict)
                json_package(diary_detailed_result["live_diary"]["live_diary_info_list"][i_list_count], "img_height",
                             "", live_diary_info_dict)
                live_diary_info_list.append(live_diary_info_dict)

            diary_detailed_dict["live_diary_info_list"] = live_diary_info_list
            request_api("/zmzx/save_shejishi_riji_xiangxi", diary_detailed_dict)
            # print("日记详细", diary_detailed_dict)


if __name__ == '__main__':
    designer_diary(104206984)
