import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from zmzx.tools.json_package import json_package
from zmzx.scheme.scheme_detailed import scheme_detailed
from zmzx.tools.request_api import request_api


def scheme_tag():
    url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/subjective-label/top-recommend"
    headers = {"X-Tingyun-Id": "7yBac11I9eg;c=2;r=550963543;",
               "platform": "android",
               "device-id": "c20964cf79411c67",
               "channelcode": "huawei",
               "sign": "",
               "If-Modified-Since": "Wed, 23 Dec 2020 07:51:03 GMT+00:00",
               "channel": "",
               "app-version": "3.2.0",
               "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; HMA-AL00 Build/LMY48Z)",
               "Host": "tuku-wap.m.jia.com",
               "Connection": "close",
               "Accept-Encoding": "gzip, deflate"}
    result = requests.get(url=url, headers=headers)
    result = json.loads(result.text)
    records_count = int(len(result["records"]))
    for r_count in range(records_count):
        base_tag = {}
        json_package(result["records"][r_count], "id", "", base_tag)
        json_package(result["records"][r_count], "cover_image_url", "", base_tag)
        json_package(result["records"][r_count], "label_name", "", base_tag)
        json_package(result["records"][r_count], "subtitle", "", base_tag)
        # print(base_tag["label_name"], "方案标签：", base_tag)
        base_tag_url = "/zmzx/save_fangan_biaoqian"
        request_api(base_tag_url, base_tag)

        #  http://tuku-wap.m.jia.com/v1.2.4/hybrid/subjective-label/detail?id=20
        base_list = {}
        base_url_list = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/subjective-label/detail?id=" + base_tag["pkey"]
        result_list = requests.get(url=base_url_list)
        result_list = json.loads(result_list.text)
        # print("result_list",result_list)
        json_package(result_list, "id", "", base_list)
        json_package(result_list, "cover_image_url", "", base_list)
        json_package(result_list, "label_name", "", base_list)
        json_package(result_list, "subtitle", "", base_list)
        result_list_count = int(len(result_list["relative_design_case_list"]))
        relative_design_case_list = []
        for r_l_count in range(result_list_count):
            relative_design_case_dict = {}
            json_package(result_list["relative_design_case_list"][r_l_count], "id", "",
                         relative_design_case_dict)
            json_package(result_list["relative_design_case_list"][r_l_count], "title", "",
                         relative_design_case_dict)
            json_package(result_list["relative_design_case_list"][r_l_count], "img_url", "",
                         relative_design_case_dict)
            json_package(result_list["relative_design_case_list"][r_l_count], "user_name", "",
                         relative_design_case_dict)
            json_package(result_list["relative_design_case_list"][r_l_count], "avatar", "",
                         relative_design_case_dict)
            json_package(result_list["relative_design_case_list"][r_l_count], "label", "",
                         relative_design_case_dict)
            # 调用方案详细
            scheme_detailed(relative_design_case_dict["pkey"])
            relative_design_case_list.append(relative_design_case_dict)
        base_list["relative_design_case_list"] = relative_design_case_list
        subjective_count = int(len(result_list["recommend_subjective_label_list"]))
        recommend_subjective_label_list = []
        for s_l_count in range(subjective_count):
            recommend_subjective_label_dict = {}
            json_package(result_list["recommend_subjective_label_list"][s_l_count], "id", "",
                         recommend_subjective_label_dict)
            json_package(result_list["recommend_subjective_label_list"][s_l_count], "label_name", "",
                         recommend_subjective_label_dict)
            recommend_subjective_label_list.append(recommend_subjective_label_dict)
        base_list["recommend_subjective_label_list"] = recommend_subjective_label_list
        # print(" 标签详情：", base_list)
        base_list_url = "/zmzx/save_fangan_biaoqian_liebiao"

        request_api(base_list_url, base_list)


if __name__ == '__main__':
    scheme_tag()
