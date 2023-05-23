import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.response_api import response_api
import math
from zmzx.tools.json_package import json_package
from tools.base64_text import text_conversion_base64
from zmzx.scheme.scheme_detailed import scheme_detailed
from zmzx.tools.request_api import request_api
from tools.handl_specialcharacters import hzs_sub


def sechme():
    url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/design-case/search"
    type_id_list = [0, 1, 2, 5]
    type_str_list = ["全部", "小编推荐", "商品优选", "小户型"]
    type_count = int(len(type_id_list))
    for type_c in range(type_count):
        # print(type_id_list[type_c])
        label_ids = type_id_list[type_c]
        indexs = type_id_list.index(label_ids)
        label_ids_str = type_str_list[indexs]
        # 全部
        # {"page_size":5,"app_version":"3.2.0","device_id":"c20964cf79411c67","sort_list":[{"category_id":-1,"category_name":"","label_ids":0}],"page_index":0,"city":"北京"}
        # 商品优选
        data = {"page_size": 10, "app_version": "3.2.0", "device_id": "c20964cf79411c67",
                "sort_list": [{"category_id": -1, "category_name": "", "label_ids": str(label_ids)}], "page_index": 0,
                "city": "北京"}
        # # 小户型
        # # {"page_size":5,"app_version":"3.2.0","device_id":"c20964cf79411c67","sort_list":[{"category_id":-1,"category_name":"","label_ids":5}],"page_index":0,"city":"北京"}
        # # 小编推荐
        # # {"page_size":5,"app_version":"3.2.0","device_id":"c20964cf79411c67","sort_list":[{"category_id":-1,"category_name":"","label_ids":1}],"page_index":0,"city":"北京"}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        result = response_api(url, headers, data)
        print(result)
        sechemCount = int(result["total_records"])
        pageCount = math.ceil(sechemCount / 10)
        if pageCount > 3:
            pageCount = 3
        # print(pageCount)
        for i in range(pageCount):
            data_page = {"page_size": 10, "app_version": "3.2.0", "device_id": "c20964cf79411c67",
                         "sort_list": [{"category_id": -1, "category_name": "", "label_ids": str(label_ids)}],
                         "page_index": str(i),
                         "city": "北京"}
            result_data_list = response_api(url, headers, data_page)
            print("方案列表原始数据:", str(result_data_list).replace("'", '"'))
            if "records" not in result_data_list:
                print("无 records 放弃本次拉取", pageCount)
                continue
            records_count = int(len(result_data_list["records"]))
            for re_count in range(records_count):
                base = {}
                print(label_ids_str, "方案共有", pageCount, "页,正在处理", i + 1, "页的第", re_count + 1, "条数据")
                json_package(result_data_list["records"][re_count], "design_fee_range", "", base)
                # 方案ID
                json_package(result_data_list["records"][re_count], "design_case_id", "", base)
                # 设计者ID
                json_package(result_data_list["records"][re_count], "designer_id", "", base)
                json_package(result_data_list["records"][re_count], "designer_name", "", base)
                json_package(result_data_list["records"][re_count], "designer_photo_url", "", base)
                json_package(result_data_list["records"][re_count], "designer_city", "", base)
                # json_package(result_data_list["records"][re_count], "title", "", base)
                # title
                base["title"] = text_conversion_base64(result_data_list["records"][re_count]["title"])
                base["sub_title"] = hzs_sub(result_data_list["records"][re_count]["title"])
                json_package(result_data_list["records"][re_count], "label_string", "", base)
                # 收藏
                json_package(result_data_list["records"][re_count], "collect_count", "", base)
                json_package(result_data_list["records"][re_count], "house_type", "", base)
                json_package(result_data_list["records"][re_count], "house_style", "", base)
                json_package(result_data_list["records"][re_count], "area", "", base)
                json_package(result_data_list["records"][re_count], "create_time", "", base)
                base["label_ids"] = label_ids_str

                json_package(result_data_list["records"][re_count], "case_cover_image", "", base)
                json_package(result_data_list["records"][re_count], "comment_count", "", base)
                json_package(result_data_list["records"][re_count], "vote_count", "", base)
                json_package(result_data_list["records"][re_count], "house_style", "", base)
                json_package(result_data_list["records"][re_count], "page_view", "", base)
                base["ext_source"] = 1
                create_time = str(base["create_time"]).replace("T", " ")
                base["create_time"] = create_time
                base["image"] = result_data_list["records"][re_count]["image"]
                url_save_list = "/zmzx/save_fangan_liebiao"
                request_api(url_save_list, base)
                # design_case_id = base["design_case_id"]
                # print("方案列表数据:", str(base).replace("'", '"'))
                # 调用方案详情功能
                scheme_detailed(str(base["design_case_id"]))


if __name__ == '__main__':
    sechme()
