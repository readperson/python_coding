import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from zmzx.tools.json_package import json_package
from tools.base64_text import text_conversion_base64
from zmzx.tools.response_api import response_api
from zmzx.tools.request_api import request_api
from zmzx.tools.designer import designer_json
from zmzx.designer.designer_detailed import designer_detailed
from zmzx.tools.comment import comment
import math
from zmzx.sunhome.sun_home_detailed import sun_home_detailed


def sun_home_tag():
    url = "http://tuku-wap.m.jia.com/v1.2.4/shc/recommend"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    reslut = requests.get(url=url)
    reslut = json.loads(reslut.text)
    print(reslut)
    records_count = int(len(reslut["records"]))
    for r_count in range(records_count):
        base = {}
        json_package(reslut["records"][r_count], "id", "", base)
        json_package(reslut["records"][r_count], "title", "", base)
        base["start_time"] = str(reslut["records"][r_count]["start_time"]).replace("T", " ")
        base["end_time"] = str(reslut["records"][r_count]["end_time"]).replace("T", " ")
        json_package(reslut["records"][r_count], "m_sub_title", "", base)
        json_package(reslut["records"][r_count], "m_description", "", base)
        base["m_description"] = text_conversion_base64(reslut["records"][r_count]["m_description"])
        json_package(reslut["records"][r_count], "cover_image_url", "", base)
        # json_package(reslut["records"][r_count], "support_count", "", base)
        # json_package(reslut["records"][r_count], "comment_count", "", base)
        # json_package(reslut["records"][r_count], "collect_count", "", base)
        # json_package(reslut["records"][r_count], "add_vote_count", "", base)

        url_list_tag = "http://tuku-wap.m.jia.com/v1.2.4/shc/detail"
        data_tag = {"page_size": 10, "campaign_id": str(base["pkey"]), "page_index": 0}
        res_tag = response_api(url_list_tag, headers, data_tag)
        base_tag_detailed = {}
        json_package(res_tag["show_home_campaign"], "id", "", base_tag_detailed)
        json_package(res_tag["show_home_campaign"], "title", "", base_tag_detailed)
        base_tag_detailed["start_time"] = str(res_tag["show_home_campaign"]["start_time"]).replace("T", " ")
        base_tag_detailed["end_time"] = str(res_tag["show_home_campaign"]["end_time"]).replace("T", " ")
        json_package(res_tag["show_home_campaign"], "m_sub_title", "", base_tag_detailed)
        json_package(res_tag["show_home_campaign"], "m_description", "", base_tag_detailed)
        base_tag_detailed["m_description"] = text_conversion_base64(res_tag["show_home_campaign"]["m_description"])
        json_package(res_tag["show_home_campaign"], "cover_image_url", "", base_tag_detailed)
        json_package(res_tag["show_home_campaign"], "cover_source", "", base_tag_detailed)
        base_tag_detailed_url = "/zmzx/save_shaijia_biaoqian"
        request_api(base_tag_detailed_url, base_tag_detailed)

        # print("晒家 标签 列表及详细", base_tag_detailed)

        # filter_types 1、精选  filter_types 2、最新
        filter_types = [1, 2]
        f_type_count = int(len(filter_types))
        for t_j in range(f_type_count):
            filter_type = filter_types[t_j]
            choiceness_url = "http://tuku-wap.m.jia.com/v1.2.4/sh/search/by/type"
            choiceness_data = {"page_size": 10, "filter_type": str(filter_type), "campaign_id": str(base["pkey"]),
                               "user_id": "",
                               "page_index": 0}
            res_choiceness_page = response_api(choiceness_url, headers, choiceness_data)
            # total_records
            pageCount = math.ceil(int(res_choiceness_page["total_records"]) / 10)
            if pageCount > 3:
                pageCount = 3
            for page in range(pageCount):
                choiceness_data_page = {"page_size": 10, "filter_type": str(filter_type),
                                        "campaign_id": str(base["pkey"]),
                                        "user_id": "",
                                        "page_index": page}
                res_choiceness = response_api(choiceness_url, headers, choiceness_data_page)
                records_count = int(len(res_choiceness["records"]))
                res_choiceness_dict = {}
                res_choiceness_dict["filter_type"] = filter_type
                res_choiceness_dict["tag_id"] = base_tag_detailed["pkey"]
                for r_choiceness_count in range(records_count):
                    print("供", pageCount, "页，正在处理第", page + 1, "页第", r_choiceness_count + 1, "条数据")
                    json_package(res_choiceness["records"][r_choiceness_count], "id", "", res_choiceness_dict)
                    res_choiceness_dict["content"] = text_conversion_base64(
                        res_choiceness["records"][r_choiceness_count]["content"])
                    json_package(res_choiceness["records"][r_choiceness_count], "user_id", "", res_choiceness_dict)
                    json_package(res_choiceness["records"][r_choiceness_count], "user_name", "", res_choiceness_dict)
                    json_package(res_choiceness["records"][r_choiceness_count], "user_photo", "", res_choiceness_dict)
                    json_package(res_choiceness["records"][r_choiceness_count], "support_count", "",
                                 res_choiceness_dict)
                    json_package(res_choiceness["records"][r_choiceness_count], "comment_count", "",
                                 res_choiceness_dict)
                    json_package(res_choiceness["records"][r_choiceness_count], "collect_count", "",
                                 res_choiceness_dict)
                    json_package(res_choiceness["records"][r_choiceness_count], "add_vote_count", "",
                                 res_choiceness_dict)
                    json_package(res_choiceness["records"][r_choiceness_count], "create_time", "", res_choiceness_dict)

                    # base["designer"] = designer_json(res_choiceness["records"][r_choiceness_count])

                    res_choiceness_dict["create_time"] = str(
                        res_choiceness["records"][r_choiceness_count]["create_time"]).replace("T", " ")
                    res_choiceness_dict["image_list"] = res_choiceness["records"][r_choiceness_count]["image_list"]
                    if "comment_list" in res_choiceness["records"][r_choiceness_count]:
                        comment_list_count = int(len(res_choiceness["records"][r_choiceness_count]["comment_list"]))
                        for c_l_count in range(comment_list_count):
                            comment_dict = comment(
                                res_choiceness["records"][r_choiceness_count]["comment_list"][c_l_count],
                                "shaijia_pkey", res_choiceness_dict["pkey"])
                            photo_url_count = int(len(comment_dict["sender_photo_url"]))
                            if photo_url_count == 0:
                                print("评论头像为空 放弃！")
                                continue
                            url_comment_dict = "/zmzx/save_shaijia_pinglun"
                            request_api(url_comment_dict, comment_dict)
                        # print("晒家评论：", comment_dict)
                    url_res_choiceness_dict = "/zmzx/save_shaijia_biaoqian_xiangxi"
                    request_api(url_res_choiceness_dict, res_choiceness_dict)
                    # 在调晒家详细单独处理
                    sun_home_detailed(res_choiceness_dict["pkey"])
                    # 调用设计者
                    designer_detailed(res_choiceness_dict["user_id"])
                # print("晒家 精选-最新 列表及详细", res_choiceness_dict)


if __name__ == '__main__':
    sun_home_tag()
