import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.response_api import response_api
import math
from zmzx.tools.json_package import json_package
from tools.base64_text import text_conversion_base64
from tools.handl_specialcharacters import hzs_sub
from zmzx.tools.comment import comment
from zmzx.tools.request_api import request_api
from zmzx.designer.dynamic_scheme_detailed import dynamic_scheme_detailed


# 动态
def designer_dynamic(user_id):

    url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/designer/action/record"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"page_size": 10, "owner_id": str(user_id), "page_index": 0}
    dynamic_list = response_api(url, headers, data)
    print("dynamic_list",dynamic_list)
    total_records = int(dynamic_list["total_records"])
    pageCount = math.ceil(total_records / 10)
    if pageCount > 3:
        pageCount = 3
    for page in range(pageCount):
        data_page = {"page_size": 10, "owner_id": str(user_id), "page_index": str(page)}
        dynamic_list_page = response_api(url, headers, data_page)
        records_count = int(len(dynamic_list_page["records"]))
        for r_count in range(records_count):
            dynamic_list_dict = {}
            print("共有动态", total_records, "条,", pageCount, "页", "正在处理第", page + 1, "页,第", r_count + 1, "条数据")
            json_package(dynamic_list_page["records"][r_count], "id", "", dynamic_list_dict)
            # json_package(dynamic_list_page["records"][r_count], "title", "", dynamic_list_dict)

            if "title" in dynamic_list_page["records"][r_count]:
                dynamic_list_dict["title"] = text_conversion_base64(
                    dynamic_list_page["records"][r_count]["title"])
            else:
                dynamic_list_dict["title"] = ""

            if "sub_title" in dynamic_list_page["records"][r_count]:
                dynamic_list_dict["sub_title"] = text_conversion_base64(
                    dynamic_list_page["records"][r_count]["sub_title"])
            else:
                dynamic_list_dict["sub_title"] = ""

            json_package(dynamic_list_page["records"][r_count], "user_id", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "user_name", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "user_identity", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "user_photo", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "page_view", "", dynamic_list_dict)
            if "image" in dynamic_list_page["records"][r_count]:
                dynamic_list_dict["image"] = dynamic_list_page["records"][r_count]["image"]
            else:
                dynamic_list_dict["image"] = {}
            json_package(dynamic_list_page["records"][r_count], "house_type", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "style", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "area", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "vote_count", "", dynamic_list_dict)
            # json_package(dynamic_list_page["records"][r_count], "comment_count", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "collection_count", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "create_time_String", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "show_home_count", "", dynamic_list_dict)
            json_package(dynamic_list_page["records"][r_count], "fans_count", "", dynamic_list_dict)
            dynamic_list_dict["create_time"] = dynamic_list_page["records"][r_count]["create_time"]
            dynamic_list_dict["comment_count"] = "0"
            vote_list_count = int(len(dynamic_list_page["records"][r_count]["vote_list"]))
            vote_list = []
            for v_l_count in range(vote_list_count):
                if dynamic_list_page["records"][r_count]["vote_list"][v_l_count] is None:
                    continue
                else:
                    vote_list.append(hzs_sub(dynamic_list_page["records"][r_count]["vote_list"][v_l_count]))
            dynamic_list_dict["vote_list"] = vote_list

            if "comment_list" in dynamic_list_page["records"][r_count]:
                comment_list_count = int(len(dynamic_list_page["records"][r_count]["comment_list"]))
                for clist_count in range(comment_list_count):
                    comment_dict = comment(dynamic_list_page["records"][r_count]["comment_list"][clist_count],
                                           "dynamic_id",
                                           dynamic_list_dict["pkey"])
                    comment_dict["data_pkey"] = dynamic_list_dict["pkey"]
                    comment_dict["type"] = "1000100"
                    photo_url_count = int(len(comment_dict["sender_photo_url"]))
                    if photo_url_count == 0:
                        print("评论头像为空 放弃！")
                        continue
                    # print("动态评论：", comment_dict)
                    request_api("/zmzx/save_ext_pinglun", comment_dict)

            # print("动态列表", dynamic_list_dict)
            request_api("/zmzx/save_shejishi_dongtai", dynamic_list_dict)
            # 动态调用方案详细
            dynamic_scheme_detailed(dynamic_list_dict["pkey"])


if __name__ == '__main__':
    designer_dynamic(105565883)
    # designer_dynamic(122904671)
