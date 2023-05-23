import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.json_package import json_package
from tools.base64_text import text_conversion_base64


def designer_json(result):
    designer = {}
    json_package(result["designer"], "id", "", designer)
    json_package(result["designer"], "user_id", "", designer)
    json_package(result["designer"], "account_name", "", designer)
    # 粉丝
    json_package(result["designer"], "follow_count", "", designer)
    # 预约
    json_package(result["designer"], "reservation_count", "", designer)
    # 案例
    json_package(result["designer"], "case_count", "", designer)
    json_package(result["designer"], "user_name", "", designer)
    json_package(result["designer"], "photo", "", designer)
    json_package(result["designer"], "city", "", designer)
    json_package(result["designer"], "phone", "", designer)
    json_package(result["designer"], "design_concept", "", designer)
    json_package(result["designer"], "max_design_fee", "", designer)
    json_package(result["designer"], "design_fee_range", "", designer)
    json_package(result["designer"], "design_fee", "", designer)
    json_package(result["designer"], "description", "", designer)
    designer["description"] = text_conversion_base64(designer["description"])
    json_package(result["designer"], "good_at_styles", "", designer)
    json_package(result["designer"], "company_address", "", designer)
    json_package(result["designer"], "designer_label", "", designer)
    if "good_at_style_list" in result["designer"]:
        designer["good_at_style_list"] = result["designer"]["good_at_style_list"]
    else:
        designer["good_at_style_list"] = []

    if "designer_label_list" in result["designer"]:
        designer["designer_label_list"] = result["designer"]["designer_label_list"]
    else:
        designer["designer_label_list"] = []

    return designer
