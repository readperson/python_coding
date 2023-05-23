import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from zmzx.tools.json_package import json_package
from tools.base64_text import text_conversion_base64
from zmzx.tools.designer import designer_json
from zmzx.tools.comment import comment
from zmzx.tools.request_api import request_api


def sun_home_detailed(s_id):
    print("-------------------------------------")
    url = "http://tuku-wap.m.jia.com/v1.2.4/sh/detail/" + str(s_id)
    result = requests.get(url=url)
    # print(result.text)
    result = json.loads(result.text)
    base = {}
    json_package(result["show_home"], "id", "", base)
    base["content"] = text_conversion_base64(result["show_home"]["content"])
    if "campaign" not in result["show_home"]:
        base["campaign"] = {}
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
        base["campaign"] = campaign
    json_package(result["show_home"], "user_id", "", base)
    json_package(result["show_home"], "user_name", "", base)
    json_package(result["show_home"], "user_photo", "", base)
    json_package(result["show_home"], "source_comment_from", "", base)
    json_package(result["show_home"], "support_count", "", base)
    json_package(result["show_home"], "works_count", "", base)
    json_package(result["show_home"], "comment_count", "", base)
    json_package(result["show_home"], "collect_count", "", base)
    json_package(result["show_home"], "add_vote_count", "", base)
    json_package(result["show_home"], "fans_count", "", base)
    json_package(result["show_home"], "show_home_count", "", base)
    base["create_time"] = str(result["show_home"]["create_time"]).replace("T", " ")
    if "designer" in result["show_home"]:
        base["designer"] = designer_json(result["show_home"])
    else:
        base["designer"] = {}
    base["image_list"] = result["show_home"]["image_list"]

    if "comment_list" in result["show_home"]:
        comment_list_count = int(len(result["show_home"]["comment_list"]))
        for c_count in range(comment_list_count):
            comment_dict = comment(result["show_home"]["comment_list"][c_count], "shaijia_pkey", base["pkey"])
            photo_url_count = int(len(comment_dict["sender_photo_url"]))
            if photo_url_count == 0:
                print("评论头像为空 放弃！")
                continue
            url_comment_dict = "/zmzx/save_shaijia_pinglun"
            request_api(url_comment_dict, comment_dict)
    #
    base_url = "/zmzx/save_shaijia_xiangxi"
    request_api(base_url, base)
    # print("晒家详细：", base)


if __name__ == '__main__':
    sun_home_detailed("132268")
