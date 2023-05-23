import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.response_api import response_api
from zmzx.tools.json_package import json_package
from zmzx.tools.designer import designer_json
from tools.base64_text import text_conversion_base64
from zmzx.tools.comment import comment
from tools.handl_specialcharacters import hzs_sub
from zmzx.tools.request_api import request_api
import math


def designer_scheme_detailed(user_id):
    url_list = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/designer/design-case/list"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data_list = {"page_size": 10, "status": 1, "user_id": str(user_id), "page_index": 0, "visitor_id": "",
                 "out_of_stock": 1}

    res_list = response_api(url_list, headers, data_list)
    pageCount = math.ceil(int(res_list["total_records"]) / 10)
    if pageCount > 3:
        pageCount = 3
    for page in range(pageCount):
        data_list_page = {"page_size": 10, "status": 1, "user_id": str(user_id), "page_index": str(page),
                          "visitor_id": "",
                          "out_of_stock": 1}
        res_list_page = response_api(url_list, headers, data_list_page)
        # print("设计者方案,列表：", res_list_page)
        if "records" not in res_list_page:
            print("records is NULL 放弃！")
            continue
        records_count = int(len(res_list_page["records"]))
        for r_ecount in range(records_count):
            print("设计师方案供", res_list["total_records"], "条数据,供", pageCount, "页正在处理第", page + 1, "页的第", r_ecount + 1,
                  "条数据")
            scheme_list_dict = {}

            json_package(res_list_page["records"][r_ecount], "design_fee_range", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "design_case_id", "", scheme_list_dict)
            scheme_list_dict["designer_id"] = user_id
            json_package(res_list_page["records"][r_ecount], "designer_photo_url", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "designer_city", "", scheme_list_dict)

            scheme_list_dict["title"] = text_conversion_base64(res_list_page["records"][r_ecount]["title"])
            scheme_list_dict["sub_title"] = hzs_sub(res_list_page["records"][r_ecount]["title"])
            json_package(res_list_page["records"][r_ecount], "label_string", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "collect_count", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "house_type", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "area", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "create_time", "", scheme_list_dict)
            scheme_list_dict["image"] = {}
            json_package(res_list_page["records"][r_ecount], "label_ids", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "case_cover_image", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "comment_count", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "vote_count", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "house_style", "", scheme_list_dict)
            json_package(res_list_page["records"][r_ecount], "page_view", "", scheme_list_dict)
            # ext_source
            scheme_list_dict["ext_source"] = 2
            # 设计者方案列表数据
            request_api("/zmzx/save_fangan_liebiao", scheme_list_dict)

            url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/design-case/find"
            data = {"design_case_id": str(scheme_list_dict["design_case_id"]), "user_id": "",
                    "device_id": "1e1080316fa234be", "app_version": "3.2.0",
                    "city": "北京"}

            result = response_api(url, headers, data)
            # print("方案明细原始数据:", str(result).replace("'", '"'))
            base = {}
            json_package(result, "id", "", base)
            json_package(result, "title", "", base)
            json_package(result, "picture_count", "", base)
            json_package(result, "house_type", "", base)
            json_package(result, "designer_id", "", base)
            json_package(result, "designer_name", "", base)
            json_package(result, "collect_count", "", base)
            base["description"] = text_conversion_base64(result["description"])
            json_package(result, "page_view", "", base)
            json_package(result, "cover_image_url", "", base)
            json_package(result, "img_width", "", base)
            json_package(result, "img_height", "", base)
            if "cover_image_description" in result:
                base["cover_image_description"] = text_conversion_base64(result["cover_image_description"])
            else:
                base["cover_image_description"] = ""
            json_package(result, "build_area", "", base)
            json_package(result, "decorate_budget", "", base)
            if "house_owner_expect" in result:
                base["house_owner_expect"] = text_conversion_base64(result["house_owner_expect"])
            else:
                base["house_owner_expect"] = ""
            json_package(result, "pre_id", "", base)
            json_package(result, "next_id", "", base)
            json_package(result, "next_title", "", base)
            # 点赞数
            json_package(result, "vote_count", "", base)
            # 评论数
            json_package(result, "comment_count", "", base)
            # 收藏数
            json_package(result, "collection_count", "", base)
            base["cover_image"] = result["cover_image"]

            base["designer"] = designer_json(result)

            # house_image_info_list
            house_image_info_list_count = int(len(result["house_image_info_list"]))
            house_image_info_list = []
            for h_l_count in range(house_image_info_list_count):
                house_image_info_dict = {}
                json_package(result["house_image_info_list"][h_l_count], "id", "", house_image_info_dict)
                json_package(result["house_image_info_list"][h_l_count], "image_url", "", house_image_info_dict)
                json_package(result["house_image_info_list"][h_l_count], "img_width", "", house_image_info_dict)
                json_package(result["house_image_info_list"][h_l_count], "img_height", "", house_image_info_dict)
            house_image_info_list.append(house_image_info_dict)

            base["house_image_info_list"] = house_image_info_list

            # effect_image_info_list
            effect_image_info_list = []
            effect_image_info_list_count = int(len(result["effect_image_info_list"]))
            for e_l_count in range(effect_image_info_list_count):
                effect_image_info_dict = {}
                json_package(result["effect_image_info_list"][e_l_count], "id", "", effect_image_info_dict)
                json_package(result["effect_image_info_list"][e_l_count], "description", "", effect_image_info_dict)
                effect_image_info_dict["description"] = text_conversion_base64(effect_image_info_dict["description"])
                json_package(result["effect_image_info_list"][e_l_count], "image_url", "", effect_image_info_dict)
                json_package(result["effect_image_info_list"][e_l_count], "img_width", "", effect_image_info_dict)
                json_package(result["effect_image_info_list"][e_l_count], "img_height", "", effect_image_info_dict)
                json_package(result["effect_image_info_list"][e_l_count], "image_space_style", "",
                             effect_image_info_dict)
                effect_image_info_list.append(effect_image_info_dict)
            base["effect_image_info_list"] = effect_image_info_list
            base["decorate_style_list"] = result["decorate_style_list"]
            base["label_info_list_obj"] = result["label_info_list_obj"]
            if "comment_list" in result:
                comment_list_count = int(len(result["comment_list"]))
                for c_count in range(comment_list_count):
                    comment_dict = comment(result["comment_list"][c_count], "design_case_id", base["pkey"])
                    photo_url_count = int(len(comment_dict["sender_photo_url"]))
                    if photo_url_count == 0:
                        print("评论头像为空 放弃！")
                        continue
                    # print("  评论：", comment_dict)
                    request_api("/zmzx/save_fangan_pinglun", comment_dict)
            # 方案详细
            request_api("/zmzx/save_fangan_xiangqing", base)
            # print("    方案详细：", base)


if __name__ == '__main__':
    designer_scheme_detailed(119789781)
