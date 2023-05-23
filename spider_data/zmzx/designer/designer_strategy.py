import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.json_package import json_package
from zmzx.tools.response_api import response_api
from tools.base64_text import text_conversion_base64
from tools.handl_specialcharacters import hzs_sub
from zmzx.tools.comment import comment
import math
from zmzx.tools.request_api import request_api


def designer_strategy(user_id):
    url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/designer/article/list/" + str(user_id)
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"page_size": 10, "app_version": "3.2.0", "page_index": 0}
    strategy_list = response_api(url, headers, data)
    total_records = int(strategy_list["total_records"])
    pageCount = math.ceil(total_records / 10)
    if pageCount > 3:
        pageCount = 3
    for page in range(pageCount):
        data_page = {"page_size": 10, "app_version": "3.2.0", "page_index": str(page)}
        strategy_list_page = response_api(url, headers, data_page)
        records_count = int(len(strategy_list_page["records"]))
        for r_count in range(records_count):
            strategy_list_dict = {}
            print("共有攻略", total_records, "条,", pageCount, "页", "正在处理第", page + 1, "页,第", r_count + 1, "条数据")
            json_package(strategy_list_page["records"][r_count], "article_id", "", strategy_list_dict)
            json_package(strategy_list_page["records"][r_count], "title", "", strategy_list_dict)
            json_package(strategy_list_page["records"][r_count], "cover_image", "", strategy_list_dict)
            json_package(strategy_list_page["records"][r_count], "page_view", "", strategy_list_dict)
            json_package(strategy_list_page["records"][r_count], "designer_id", "", strategy_list_dict)
            strategy_list_dict["description"] = text_conversion_base64(
                strategy_list_page["records"][r_count]["description"])
            json_package(strategy_list_page["records"][r_count], "collect_count", "", strategy_list_dict)
            json_package(strategy_list_page["records"][r_count], "product_count", "", strategy_list_dict)
            json_package(strategy_list_page["records"][r_count], "comment_count", "", strategy_list_dict)
            json_package(strategy_list_page["records"][r_count], "vote_count", "", strategy_list_dict)
            strategy_list_dict["image"] = strategy_list_page["records"][r_count]["image"]
            # 攻略列表
            request_api("/zmzx/save_shejishi_gonglue", strategy_list_dict)
            # print("攻略列表", strategy_list_dict)

            # 攻略详细
            url_detailed = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/article/detail"
            data_detailed = {"user_id": "", "article_id": str(strategy_list_dict["article_id"]),
                             "device_id": "1e1080316fa234be",
                             "app_version": "3.2.0"}
            detailed_result = response_api(url_detailed, headers, data_detailed)
            strategy_detailed_dict = {}
            json_package(detailed_result, "id", "", strategy_detailed_dict)
            json_package(detailed_result, "title", "", strategy_detailed_dict)
            if "sub_title" in detailed_result:
                strategy_detailed_dict["sub_title"] = text_conversion_base64(detailed_result["sub_title"])
            else:
                strategy_detailed_dict["sub_title"] = ""
            json_package(detailed_result, "page_view", "", strategy_detailed_dict)
            strategy_detailed_dict["image"] = detailed_result["image"]
            json_package(detailed_result, "collect_count", "", strategy_detailed_dict)
            json_package(detailed_result, "comment_count", "", strategy_detailed_dict)
            json_package(detailed_result, "designer_id", "", strategy_detailed_dict)
            json_package(detailed_result, "user_photo", "", strategy_detailed_dict)
            json_package(detailed_result, "user_name", "", strategy_detailed_dict)
            json_package(detailed_result, "vote_count", "", strategy_detailed_dict)
            # record_list
            record_list_count = int(len(detailed_result["record_list"]))
            record_list = []
            for r_list_count in range(record_list_count):
                record_dict = {}
                json_package(detailed_result["record_list"][r_list_count], "id", "", record_dict)
                record_dict["main_body"] = text_conversion_base64(
                    detailed_result["record_list"][r_list_count]["main_body"])
                record_dict["image"] = detailed_result["record_list"][r_list_count]["image"]
                record_list.append(record_dict)
            strategy_detailed_dict["record_list"] = record_list
            if "comment_list" in detailed_result:
                comment_list_count = int(len(detailed_result["comment_list"]))
                for c_list_count in range(comment_list_count):
                    comment_dict = comment(detailed_result["comment_list"][c_list_count], "strategy_id",
                                           strategy_detailed_dict["pkey"])
                    comment_dict["data_pkey"] = strategy_detailed_dict["pkey"]
                    comment_dict["type"] = "1000300"
                    photo_url_count = int(len(comment_dict["sender_photo_url"]))
                    if photo_url_count == 0:
                        print("评论头像为空 放弃！")
                        continue
                    # print("攻略略评论：", comment_dict)
                    request_api("/zmzx/save_ext_pinglun", comment_dict)

            # print(" 攻略详细：", strategy_detailed_dict)
            # 攻略详细
            request_api("/zmzx/save_shejishi_gonglue_xiangqing", strategy_detailed_dict)


if __name__ == '__main__':
    # designer_strategy(105565883)
    designer_strategy(111326006)
