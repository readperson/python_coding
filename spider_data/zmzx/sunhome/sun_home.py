import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.response_api import response_api
from tools.base64_text import text_conversion_base64
from zmzx.tools.comment import comment
from tools.handl_specialcharacters import hzs_sub
import math
from zmzx.tools.json_package import json_package
from zmzx.tools.design_case_lists import design_case
from zmzx.tools.designer_lists import designer
from zmzx.sunhome.sun_home_detailed import sun_home_detailed
from zmzx.designer.designer_detailed import designer_detailed
from zmzx.tools.request_api import request_api


def sunhome():
    url = "http://tuku-wap.m.jia.com/v1.2.4/sh/search"
    data = {"page_size": 10, "user_id": "", "page_index": 0}
    headers = {"Content-Type": "application/json;charset=utf-8"}
    result = response_api(url, headers, data)
    total_records = result["total_records"]
    pageCount = math.ceil(total_records / 10)
    if pageCount > 3:
        pageCount = 3
    id_list = []
    # user_id_list = []
    for p in range(pageCount):
        page_data = {"page_size": 10, "user_id": "", "page_index": str(p)}
        result_list = response_api(url, headers, page_data)
        if "records" not in result_list:
            # designer(user_id_list)
            # design_case(id_list)
            print("无 records 放弃本次拉取", pageCount)
            break
        records_count = int(len(result_list["records"]))
        for r_count in range(records_count):
            print("晒家共有", pageCount, "页,正在处理", p + 1, "页的第", r_count + 1, "条数据")
            base = {}
            # 晒家ID
            json_package(result_list["records"][r_count], "id", "", base)
            id_list.append(base["pkey"])
            base["content"] = text_conversion_base64(result_list["records"][r_count]["content"])
            base["sub_title"] = hzs_sub(result_list["records"][r_count]["content"])
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
            # id = base["pkey"]
            # id_list.append(id)
            # user_id = base["user_id"]
            # user_id_list.append(user_id)
            if "campaign" not in result_list["records"][r_count]:
                base["campaign"] = {}
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
                for c_count in range(comment_list_count):
                    comment_dict = comment(result_list["records"][r_count]["comment_list"][c_count], "shaijia_pkey",
                                           base["pkey"])
                    photo_url_count = int(len(comment_dict["sender_photo_url"]))
                    if photo_url_count == 0:
                        print("评论头像为空 放弃！")
                        continue
                    url_comment_dict = "/zmzx/save_shaijia_pinglun"
                    request_api(url_comment_dict, comment_dict)
                # comment_list = []
            # base["comment_list"] = comment_list
            # 列表
            base_url = "/zmzx/save_shaijia_liebiao"
            request_api(base_url, base)
            # 调用晒家详细
            sun_home_detailed(base["pkey"])
            # 调用设计者
            designer_detailed(base["user_id"])
    # print(id_list)


if __name__ == '__main__':
    sunhome()
