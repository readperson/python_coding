import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.response_api import response_api
import math
from zmzx.tools.json_package import json_package
from tools.base64_text import text_conversion_base64
from zmzx.designer.designer_detailed import designer_detailed
from zmzx.tools.request_api import request_api
import random


# 105565883

def designer():
    url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/find-designer/search"
    data = {"style_list": [], "city": "北京", "design_fee_list": [], "identity_list": [], "page_index": 0,
            "page_size": 40}
    headers = {"Content-Type": "application/json;charset=utf-8"}
    res_designer_list = response_api(url, headers, data)
    print("res_designer_list", res_designer_list)
    total_records = res_designer_list["total_records"]
    pageCount = math.ceil(total_records / 40)
    if pageCount > 2:
        pageCount = 2
    # start_time = now_timestamp()
    for page in range(pageCount):
        data_page = {"style_list": [], "city": "北京", "design_fee_list": [], "identity_list": [],
                     "page_index": str(page),
                     "page_size": 40}
        res_designer_list_page = response_api(url, headers, data_page)
        print("res_designer_list_page", res_designer_list_page)
        records_count = int(len(res_designer_list_page["records"]))
        for r_count in range(records_count):
            print("========================================共有设计师", total_records, "人,", pageCount, "页", "正在处理第",
                  page + 1, "页,第", r_count + 1, "条数据==================================")
            base = {}
            json_package(res_designer_list_page["records"][r_count], "designer_id", "", base)
            json_package(res_designer_list_page["records"][r_count], "designer_name", "", base)
            json_package(res_designer_list_page["records"][r_count], "city", "", base)
            json_package(res_designer_list_page["records"][r_count], "designFee", "", base)
            designFee = str(res_designer_list_page["records"][r_count]["designFee"]).split("~")
            designFee_count = int(len(designFee))
            # print("designFee", designFee)
            if designFee_count == 1:
                base["design_fee"] = "0"
                base["max_design_fee"] = "0"
            else:
                base["design_fee"] = designFee[0]
                base["max_design_fee"] = designFee[1]

            json_package(res_designer_list_page["records"][r_count], "designer_photo_url", "", base)
            json_package(res_designer_list_page["records"][r_count], "reservation_quantity", "", base)
            json_package(res_designer_list_page["records"][r_count], "is_golden_designer", "", base)
            json_package(res_designer_list_page["records"][r_count], "follow_count", "", base)
            json_package(res_designer_list_page["records"][r_count], "design_case_count", "", base)
            json_package(res_designer_list_page["records"][r_count], "article_count", "", base)
            json_package(res_designer_list_page["records"][r_count], "show_home_count", "", base)
            json_package(res_designer_list_page["records"][r_count], "live_diary_count", "", base)
            json_package(res_designer_list_page["records"][r_count], "all_product_collect_count", "", base)
            # 作品
            json_package(res_designer_list_page["records"][r_count], "all_product_count", "", base)
            json_package(res_designer_list_page["records"][r_count], "company_name", "", base)
            # identity 等于3的时候需要做特殊处理
            ints = random.randint(1, 3)
            identity = int(res_designer_list_page["records"][r_count]["identity"])
            # print(identity)
            # print(ints)
            if identity == 3 and ints == 3:
                base["identity"] = "1"
            else:
                base["identity"] = str(identity)
            if "good_at_style_list" in res_designer_list_page["records"][r_count]:
                base["good_at_style_list"] = res_designer_list_page["records"][r_count]["good_at_style_list"]
            else:
                base["good_at_style_list"] = []
            if "designer_label_list" in res_designer_list_page["records"][r_count]:
                base["designer_label_list"] = res_designer_list_page["records"][r_count]["designer_label_list"]
            else:
                base["designer_label_list"] = []

            # designer_production_list
            designer_production_list = []
            if "designer_production_list" in res_designer_list_page["records"][r_count]:
                production_count = int(len(res_designer_list_page["records"][r_count]["designer_production_list"]))
                for pn_count in range(production_count):
                    designer_production_dict = {}
                    json_package(res_designer_list_page["records"][r_count]["designer_production_list"][pn_count], "id",
                                 "",
                                 designer_production_dict)
                    json_package(res_designer_list_page["records"][r_count]["designer_production_list"][pn_count],
                                 "type",
                                 "", designer_production_dict)
                    if "" in res_designer_list_page["records"][r_count]["designer_production_list"][pn_count]:
                        designer_production_dict["title"] = text_conversion_base64(
                            res_designer_list_page["records"][r_count]["designer_production_list"][pn_count]["title"])
                    else:
                        designer_production_dict["title"] = ""
                    json_package(res_designer_list_page["records"][r_count]["designer_production_list"][pn_count],
                                 "cover_url", "", designer_production_dict)
                    json_package(res_designer_list_page["records"][r_count]["designer_production_list"][pn_count],
                                 "page_view", "", designer_production_dict)
                    json_package(res_designer_list_page["records"][r_count]["designer_production_list"][pn_count],
                                 "collect_count", "", designer_production_dict)
                    json_package(res_designer_list_page["records"][r_count]["designer_production_list"][pn_count],
                                 "style",
                                 "", designer_production_dict)
                    json_package(res_designer_list_page["records"][r_count]["designer_production_list"][pn_count],
                                 "house_type", "", designer_production_dict)
                    json_package(res_designer_list_page["records"][r_count]["designer_production_list"][pn_count],
                                 "area",
                                 "", designer_production_dict)
                    designer_production_list.append(designer_production_dict)
            else:
                designer_production_list = []
            base["designer_production_list"] = designer_production_list
            if "label_list" in res_designer_list_page["records"][r_count]:
                base["label_list"] = res_designer_list_page["records"][r_count]["label_list"]
            else:
                base["label_list"] = []
            request_api("/zmzx/save_shejishi_liebiao", base)
            # 设计师明细
            designer_detailed(base["designer_id"])
            # print("base:", base)

    # end_time = now_timestamp()
    # t_m = end_time - start_time
    # print("###################处理时长############", t_m)


if __name__ == '__main__':
    designer()
