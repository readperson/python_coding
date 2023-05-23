import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from zmzx.tools.json_package import json_package
from tools.base64_text import text_conversion_base64
from tools.handl_specialcharacters import hzs_sub
from zmzx.tools.response_api import response_api
import math
from zmzx.tools.designer import designer_json
from zmzx.tools.comment import comment
from zmzx.tools.request_api import request_api


def designer_sun_home_detailed(user_id):
    url_list = "http://tuku-wap.m.jia.com/v1.2.4/sh/someone/search"
    data_list = {"page_size": 10, "owner_id": str(user_id), "user_id": "", "page_index": 0, "sort_type": "desc"}
    headers = {"Content-Type": "application/json;charset=utf-8"}
    result_li = response_api(url_list, headers, data_list)
    total_records = result_li["total_records"]
    pageCount = math.ceil(total_records / 10)
    if pageCount > 3:
        pageCount = 3
    for p in range(pageCount):
        page_data = {"page_size": 10, "owner_id": str(user_id), "user_id": "", "page_index": str(p),
                     "sort_type": "desc"}
        result_list = response_api(url_list, headers, page_data)
        if "records" not in result_list:
            # designer(user_id_list)
            # design_case(id_list)
            print("无 records 放弃本次拉取", pageCount)
            break
        records_count = int(len(result_list["records"]))
        for r_count in range(records_count):
            print("晒家", total_records, "条记录共有", pageCount, "页,正在处理", p + 1, "页的第", r_count + 1, "条数据")
            base = {}
            # 晒家ID
            json_package(result_list["records"][r_count], "id", "", base)
            base["content"] = text_conversion_base64(result_list["records"][r_count]["content"])
            # 设计者ID
            json_package(result_list["records"][r_count], "user_id", "", base)
            json_package(result_list["records"][r_count], "user_name", "", base)
            json_package(result_list["records"][r_count], "user_photo", "", base)
            json_package(result_list["records"][r_count], "source_id", "", base)
            # 收藏
            json_package(result_list["records"][r_count], "support_count", "", base)
            # 评论
            json_package(result_list["records"][r_count], "comment_count", "", base)
            # 点赞
            json_package(result_list["records"][r_count], "collect_count", "", base)
            json_package(result_list["records"][r_count], "add_vote_count", "", base)
            json_package(result_list["records"][r_count], "source_id", "", base)
            json_package(result_list["records"][r_count], "source_id", "", base)
            json_package(result_list["records"][r_count], "source_id", "", base)
            json_package(result_list["records"][r_count], "create_time", "", base)
            base["create_time"] = str(base["create_time"]).replace("T", " ")
            if "campaign" not in result_list["records"][r_count]:
                base["campaign"] = ""
            else:
                # base["campaign"] = result_list["records"][r_count]["campaign"]
                campaign = {}
                json_package(result_list["records"][r_count]["campaign"], "id", "", campaign)
                json_package(result_list["records"][r_count]["campaign"], "title", "", campaign)
                # json_package(result_list["records"][r_count]["campaign"], "start_time", "", campaign)
                campaign["start_time"] = str(result_list["records"][r_count]["campaign"]["start_time"]).replace("T",
                                                                                                                " ")

                # json_package(result_list["records"][r_count]["campaign"], "end_time", "", campaign)
                campaign["end_time"] = str(result_list["records"][r_count]["campaign"]["end_time"]).replace("T", " ")
                json_package(result_list["records"][r_count]["campaign"], "m_description", "", campaign)
                campaign["m_description"] = text_conversion_base64(campaign["m_description"])
                json_package(result_list["records"][r_count]["campaign"], "cover_image_url", "", campaign)
                base["campaign"] = campaign
            base["image_list"] = result_list["records"][r_count]["image_list"]
            if "comment_list" in result_list["records"][r_count]:
                comment_list_count = int(len(result_list["records"][r_count]["comment_list"]))
                for c_list_count in range(comment_list_count):
                    comment_dict = comment(result_list["records"][r_count]["comment_list"][c_list_count], "shaijia_pkey",
                                           base["pkey"])
                    photo_url_count = int(len(comment_dict["sender_photo_url"]))
                    if photo_url_count == 0:
                        print("评论头像为空 放弃！")
                        continue
                    request_api("/zmzx/save_shaijia_pinglun", comment_dict)
            # 晒家列表
            request_api("/zmzx/save_shaijia_liebiao", base)
            # print("晒家列表", base)

            url = "http://tuku-wap.m.jia.com/v1.2.4/sh/detail/" + str(base["pkey"])
            result = requests.get(url=url)
            # print(result.text)
            result = json.loads(result.text)
            base_detailed = {}
            json_package(result["show_home"], "id", "", base_detailed)
            base_detailed["content"] = text_conversion_base64(result["show_home"]["content"])
            if "campaign" not in result["show_home"]:
                base_detailed["campaign"] = ""
            else:
                campaign = {}
                json_package(result["show_home"]["campaign"], "id", "", campaign)
                json_package(result["show_home"]["campaign"], "title", "", campaign)
                campaign["start_time"] = str(result["show_home"]["campaign"]["start_time"]).replace("T", " ")

                # json_package(result["show_home"], "end_time", "", campaign)
                # campaign["end_time"] = str(campaign["end_time"]).replace("T", " ")
                campaign["end_time"] = str(result["show_home"]["campaign"]["end_time"]).replace("T", " ")
                json_package(result["show_home"]["campaign"], "m_description", "", campaign)
                campaign["m_description"] = text_conversion_base64(campaign["m_description"])
                json_package(result["show_home"]["campaign"], "cover_image_url", "", campaign)
                base_detailed["campaign"] = campaign
            json_package(result["show_home"], "user_id", "", base_detailed)
            json_package(result["show_home"], "user_name", "", base_detailed)
            json_package(result["show_home"], "user_photo", "", base_detailed)
            json_package(result["show_home"], "source_comment_from", "", base_detailed)
            json_package(result["show_home"], "support_count", "", base_detailed)
            json_package(result["show_home"], "works_count", "", base_detailed)
            json_package(result["show_home"], "comment_count", "", base_detailed)
            json_package(result["show_home"], "collect_count", "", base_detailed)
            json_package(result["show_home"], "add_vote_count", "", base_detailed)
            json_package(result["show_home"], "fans_count", "", base_detailed)
            json_package(result["show_home"], "show_home_count", "", base_detailed)
            base_detailed["create_time"] = str(result["show_home"]["create_time"]).replace("T", " ")
            if "designer" in result["show_home"]:
                base_detailed["designer"] = designer_json(result["show_home"])
            else:
                base_detailed["designer"] = {}
            base_detailed["image_list"] = result["show_home"]["image_list"]

            if "comment_list" in result["show_home"]:
                comment_list_count = int(len(result["show_home"]["comment_list"]))
                for c_count in range(comment_list_count):
                    comment_dict = comment(result["show_home"]["comment_list"][c_count], "shaijia_pkey", base["pkey"])
                    photo_url_count = int(len(comment_dict["sender_photo_url"]))
                    if photo_url_count == 0:
                        print("评论头像为空 放弃！")
                        continue
                    # print("晒家评论：", comment_dict)
                    request_api("/zmzx/save_shaijia_pinglun", comment_dict)
            # 晒家详细
            request_api("/zmzx/save_shaijia_xiangxi", base_detailed)

            # print("晒家详细：", base_detailed)


if __name__ == '__main__':
    designer_sun_home_detailed("119753704")
