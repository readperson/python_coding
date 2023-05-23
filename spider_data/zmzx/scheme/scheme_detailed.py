import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.response_api import response_api
from zmzx.tools.json_package import json_package
from zmzx.tools.designer import designer_json
from tools.base64_text import text_conversion_base64
from zmzx.tools.comment import comment
from zmzx.tools.request_api import request_api
from zmzx.designer.designer_detailed import designer_detailed


def scheme_detailed(design_case_id):
    url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/design-case/find"
    data = {"design_case_id": str(design_case_id), "user_id": "", "device_id": "c20964cf79411c67",
            "app_version": "3.2.0",
            "city": "北京"}
    headers = {"Content-Type": "application/json;charset=utf-8"}
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
        json_package(result["effect_image_info_list"][e_l_count], "image_space_style", "", effect_image_info_dict)
        effect_image_info_list.append(effect_image_info_dict)
    base["effect_image_info_list"] = effect_image_info_list
    base["decorate_style_list"] = result["decorate_style_list"]
    base["label_info_list_obj"] = result["label_info_list_obj"]
    # comment_list
    # comment_list = []
    if "comment_list" in result:
        comment_list_count = int(len(result["comment_list"]))
        for c_count in range(comment_list_count):
            comment_dict = comment(result["comment_list"][c_count], "design_case_id", base["pkey"])
            photo_url_count = int(len(comment_dict["sender_photo_url"]))
            if photo_url_count == 0:
                print("评论头像为空 放弃！")
                continue
            url_comment = "/zmzx/save_fangan_pinglun"
            request_api(url_comment, comment_dict)
            # print("  评论：", comment_dict)
    url_save_detailed = "/zmzx/save_fangan_xiangqing"
    request_api(url_save_detailed, base)
    # 调用设计者详细功能
    designer_detailed(str(base["designer_id"]))
    # print("    方案详细：", base)


if __name__ == '__main__':
    scheme_detailed(45620)
