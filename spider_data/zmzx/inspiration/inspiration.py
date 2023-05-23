import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from zmzx.tools.response_api import response_api
import math
from zmzx.tools.json_package import json_package
from tools.base64_text import text_conversion_base64
from zmzx.tools.comment import comment
from zmzx.designer.designer_detailed import designer_detailed
from zmzx.tools.request_api import request_api


# 灵感
def inspiration_tag():
    url_tag = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/hpi/label"
    result = requests.get(url=url_tag)
    # print(result.text)
    result = json.loads(result.text)
    label_count = int(len(result["label_info_list"]))
    for l_count in range(label_count):
        label_info_dict = {}
        json_package(result["label_info_list"][l_count], "id", "", label_info_dict)
        json_package(result["label_info_list"][l_count], "category_id", "", label_info_dict)
        json_package(result["label_info_list"][l_count], "label_id", "", label_info_dict)
        json_package(result["label_info_list"][l_count], "label_name", "", label_info_dict)
        # print("找灵感标签：", label_info_dict)
        # /zmzx/save_linggan_biaoqian
        url_label_info_dict = "/zmzx/save_linggan_biaoqian"
        request_api(url_label_info_dict, label_info_dict)
        # {'pkey': '18', 'category_id': '5', 'label_id': '18', 'label_name': '客厅'}
        url_tag_list = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/hpi/search"
        url_tag_data = {"page_size": 10, "category_id": label_info_dict["category_id"], "design_case_id": "0",
                        "page_index": 0,
                        "label_id": label_info_dict["label_id"]}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        tag_result = response_api(url_tag_list, headers, url_tag_data)
        # print(tag_result)
        # total_records
        total_records = int(tag_result["total_records"])
        pageCount = math.ceil(total_records / 10)
        if pageCount > 3:
            pageCount = 3
        for page in range(pageCount):
            url_tag_data_page = {"page_size": 10, "category_id": label_info_dict["category_id"], "design_case_id": "0",
                                 "page_index": str(page),
                                 "label_id": label_info_dict["label_id"]}
            tag_page_result = response_api(url_tag_list, headers, url_tag_data_page)
            records_count = int(len(tag_page_result["records"]))
            for r_count in range(records_count):
                print(label_info_dict["label_name"], "共有", total_records, "条记录", pageCount, "页", "正在处理第", page + 1, "第",
                      r_count + 1, "条数据")
                tag_list_dict = {}
                tag_list_dict["label_id"] = label_info_dict["pkey"]
                tag_list_dict["label_name"] = label_info_dict["label_name"]
                json_package(tag_page_result["records"][r_count], "id", "", tag_list_dict)
                json_package(tag_page_result["records"][r_count], "description", "", tag_list_dict)
                tag_list_dict["description"] = text_conversion_base64(
                    tag_page_result["records"][r_count]["description"])
                json_package(tag_page_result["records"][r_count], "image_url", "", tag_list_dict)
                json_package(tag_page_result["records"][r_count], "img_width", "", tag_list_dict)
                json_package(tag_page_result["records"][r_count], "img_height", "", tag_list_dict)
                # 设计师ID
                json_package(tag_page_result["records"][r_count], "user_id", "", tag_list_dict)
                json_package(tag_page_result["records"][r_count], "user_name", "", tag_list_dict)
                json_package(tag_page_result["records"][r_count], "user_avatar", "", tag_list_dict)
                #                 label_info_obj_list
                tag_list_dict["label_info_obj_list"] = tag_page_result["records"][r_count]["label_info_obj_list"]

                # print("   找灵感标签列表：", tag_list_dict)
                url_tag_list_dict = "/zmzx/save_linggan_liebiao"
                request_api(url_tag_list_dict, tag_list_dict)

                #               http://tuku-wap.m.jia.com/v1.2.4/hybrid/hpi/find/detail
                #               {"comment_size":0,"id":"1714958","user_id":""}
                tag_detailed_url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/hpi/find/detail"
                tag_detailed_data = {"comment_size": 0, "id": tag_list_dict["pkey"], "user_id": ""}
                tag_detailed_result = response_api(tag_detailed_url, headers, tag_detailed_data)
                # print("--------",tag_detailed_result)
                detailed_base = {}
                json_package(tag_detailed_result, "id", "", detailed_base)
                detailed_base["user_id"] = tag_list_dict["user_id"]
                # json_package(tag_detailed_result, "id", "", detailed_base)
                json_package(tag_detailed_result, "image_url", "", detailed_base)
                json_package(tag_detailed_result, "img_width", "", detailed_base)
                json_package(tag_detailed_result, "img_height", "", detailed_base)
                # "vote_count": 0,
                # "comment_count": 0,
                json_package(tag_detailed_result, "vote_count", "", detailed_base)
                json_package(tag_detailed_result, "comment_count", "", detailed_base)
                json_package(tag_detailed_result, "collection_count", "", detailed_base)
                detailed_base["description"] = text_conversion_base64(tag_detailed_result["description"])
                json_package(tag_detailed_result, "next_id", "", detailed_base)

                design_case_detail = {}
                json_package(tag_detailed_result["design_case_detail"], "id", "", design_case_detail)
                json_package(tag_detailed_result["design_case_detail"], "title", "", design_case_detail)
                json_package(tag_detailed_result, "picture_count", "", design_case_detail)
                json_package(tag_detailed_result["design_case_detail"], "house_type", "", design_case_detail)
                json_package(tag_detailed_result["design_case_detail"], "cover_image_url", "", design_case_detail)
                json_package(tag_detailed_result["design_case_detail"], "build_area", "", design_case_detail)
                detailed_base["design_case_detail"] = design_case_detail

                designer = {}
                json_package(tag_detailed_result["design_case_detail"]["designer"], "id", "", designer)
                # 粉丝数
                json_package(tag_detailed_result["design_case_detail"]["designer"], "follow_count", "", designer)
                # 预约数
                json_package(tag_detailed_result["design_case_detail"]["designer"], "reservation_count", "", designer)
                # 案例数
                json_package(tag_detailed_result["design_case_detail"]["designer"], "case_count", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "user_id", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "account_name", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "user_name", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "photo", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "city", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "phone", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "design_concept", "", designer)
                if "description" in tag_detailed_result["design_case_detail"]["designer"]:
                    designer["description"] = text_conversion_base64(
                        tag_detailed_result["design_case_detail"]["designer"]["description"])
                else:
                    designer["description"] = ""

                json_package(tag_detailed_result["design_case_detail"]["designer"], "design_fee", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "max_design_fee", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "design_fee_range", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "serve_city", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "good_at_styles", "", designer)
                json_package(tag_detailed_result["design_case_detail"]["designer"], "company_address", "", designer)
                if "card_activation_time" in tag_detailed_result["design_case_detail"]["designer"]:
                    designer["card_activation_time"] = str(
                        tag_detailed_result["design_case_detail"]["designer"]["card_activation_time"]).replace("T", " ")
                else:
                    designer["card_activation_time"] = ""

                if "good_at_style_list" in tag_detailed_result["design_case_detail"]["designer"]:
                    designer["good_at_style_list"] = tag_detailed_result["design_case_detail"]["designer"][
                        "good_at_style_list"]
                else:
                    designer["good_at_style_list"] = []

                design_case_detail["designer"] = designer
                design_case_detail["decorate_style_list"] = tag_detailed_result["design_case_detail"][
                    "decorate_style_list"]

                # comment_list
                if "comment_list" in tag_detailed_result:
                    comment_list_count = int(len(tag_detailed_result["comment_list"]))
                    for c_l_count in range(comment_list_count):
                        comment_dict = comment(tag_detailed_result["comment_list"][c_l_count], "linggan_pkey",
                                               detailed_base["pkey"])
                        photo_url_count = int(len(comment_dict["sender_photo_url"]))
                        if photo_url_count == 0:
                            print("评论头像为空 放弃！")
                            continue
                        url_comment_dict = "/zmzx/save_linggan_pinglun"
                        request_api(url_comment_dict, comment_dict)
                        # print("   灵感评论：", comment_dict)

                detailed_base["design_case_detail"] = design_case_detail
                url_design_case_detail = "/zmzx/save_linggan_xiangxi"
                request_api(url_design_case_detail, detailed_base)
                # 调用设计者：
                designer_detailed(tag_list_dict["user_id"])
                # print("       找灵感详细", detailed_base)


if __name__ == '__main__':
    inspiration_tag()
