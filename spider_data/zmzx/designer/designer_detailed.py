import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from zmzx.tools.json_package import json_package
from tools.base64_text import text_conversion_base64
from zmzx.designer.designer_dynamic import designer_dynamic
from zmzx.designer.designer_scheme import designer_scheme_detailed
from zmzx.designer.designer_diary import designer_diary
from zmzx.designer.designer_sunhome import designer_sun_home_detailed
from zmzx.designer.designer_strategy import designer_strategy
import threading
from zmzx.tools.request_api import request_api


def designer_detailed(designer_id):
    # 设计师个人信息
    url = "http://tuku-wap.m.jia.com/v1.2.4/hybrid/designer/detail?designerId=" + str(
        designer_id) + "&userId=0&appVersion=3.2.0"
    designer_info = requests.get(url=url)
    # print("设计师原始数据：", designer_info.text)
    # start_time = now_timestamp()
    if int(len(designer_info.text)) > 0:
        designer_info = json.loads(designer_info.text)
        designer_info_dict = {}
        json_package(designer_info, "id", "", designer_info_dict)
        json_package(designer_info, "user_id", "", designer_info_dict)
        json_package(designer_info, "account_name", "", designer_info_dict)
        json_package(designer_info, "user_name", "", designer_info_dict)
        json_package(designer_info, "photo", "", designer_info_dict)
        json_package(designer_info, "phone", "", designer_info_dict)
        designer_info_dict["design_concept"] = text_conversion_base64(designer_info["design_concept"])
        # designer_info_dict["design_concept"] = (designer_info["design_concept"])
        if "description" in designer_info:
            designer_info_dict["description"] = text_conversion_base64(designer_info["description"])
        else:
            designer_info_dict["description"] = ""
        # designer_info_dict["description"] = (designer_info["description"])
        json_package(designer_info, "design_fee", "", designer_info_dict)
        json_package(designer_info, "max_design_fee", "", designer_info_dict)
        json_package(designer_info, "design_fee_range", "", designer_info_dict)
        json_package(designer_info, "remote_design_fee", "", designer_info_dict)
        json_package(designer_info, "max_remote_design_fee", "", designer_info_dict)
        json_package(designer_info, "remote_design_fee_range", "", designer_info_dict)
        json_package(designer_info, "serve_city", "", designer_info_dict)
        json_package(designer_info, "reservation_count", "", designer_info_dict)
        # 作品
        json_package(designer_info, "case_count", "", designer_info_dict)
        json_package(designer_info, "good_at_styles", "", designer_info_dict)
        # 粉丝
        json_package(designer_info, "following_count", "", designer_info_dict)
        json_package(designer_info, "follow_count", "", designer_info_dict)
        json_package(designer_info, "production_count", "", designer_info_dict)
        json_package(designer_info, "inspiration_count", "", designer_info_dict)
        json_package(designer_info, "strategy_count", "", designer_info_dict)
        json_package(designer_info, "show_home_count", "", designer_info_dict)
        json_package(designer_info, "show_home_vote_total_count", "", designer_info_dict)
        json_package(designer_info, "show_home_collect_total_count", "", designer_info_dict)
        json_package(designer_info, "tea_home_total", "", designer_info_dict)
        json_package(designer_info, "company_address", "", designer_info_dict)
        json_package(designer_info, "score", "", designer_info_dict)
        json_package(designer_info, "live_diary_amount", "", designer_info_dict)
        if "designer_label" in designer_info:
            designer_info_dict["designer_label"] = text_conversion_base64(designer_info["designer_label"])
        else:
            designer_info_dict["designer_label"] = ""
        json_package(designer_info, "portrait", "", designer_info_dict)
        json_package(designer_info, "identity", "", designer_info_dict)
        json_package(designer_info, "wechat", "", designer_info_dict)
        json_package(designer_info, "email", "", designer_info_dict)
        json_package(designer_info, "work_years", "", designer_info_dict)
        json_package(designer_info, "company_name", "", designer_info_dict)
        json_package(designer_info, "designer_count", "", designer_info_dict)
        if "card_activation_time" in designer_info:
            designer_info_dict["card_activation_time"] = str(designer_info["card_activation_time"]).replace("T", " ")
        else:
            designer_info_dict["card_activation_time"] = ""

        json_package(designer_info, "influence", "", designer_info_dict)
        json_package(designer_info, "influence_percent", "", designer_info_dict)
        if "good_at_style_list" in designer_info:
            designer_info_dict["good_at_style_list"] = designer_info["good_at_style_list"]
        else:
            designer_info_dict["good_at_style_list"] = []

        if "designer_label_list" in designer_info:
            designer_info_dict["designer_label_list"] = designer_info["designer_label_list"]
        else:
            designer_info_dict["designer_label_list"] = []
        designer_info_dict["award_list"] = designer_info["award_list"]

        # 设计师个人信息
        request_api("/zmzx/save_shejishi_xiangxi", designer_info_dict)
        # 设计师动态
        designer_dynamic(designer_info_dict["user_id"])
        # 设计师方案
        designer_scheme_detailed(designer_info_dict["user_id"])
        # 设计师晒家
        designer_sun_home_detailed(designer_info_dict["user_id"])
        # 设计师日记
        designer_diary(designer_info_dict["user_id"])
        # 设计师攻略
        designer_strategy(designer_info_dict["user_id"])

        # # 调用动态
        # t1 = threading.Thread(target=designer_dynamic, args=(designer_info_dict["user_id"],))
        # # 设计师方案明细
        # t2 = threading.Thread(target=designer_scheme_detailed, args=(designer_info_dict["user_id"],))
        # # 设计晒家明细
        # t3 = threading.Thread(target=designer_sun_home_detailed, args=(designer_info_dict["user_id"],))
        # # 调用日记
        # t4 = threading.Thread(target=designer_diary, args=(designer_info_dict["user_id"],))
        # # 攻略
        # t5 = threading.Thread(target=designer_strategy, args=(designer_info_dict["user_id"],))
        # t1.start()
        # t2.start()
        # t3.start()
        # t4.start()
        # t5.start()
    else:
        print("设计师ID=================", designer_id, "异常")
    # end_time = now_timestamp()
    # t_m = end_time - start_time


if __name__ == '__main__':
    # designer_detailed(105565883)
    # designer_detailed(117781812)
    # designer_detailed(120413744)
    designer_detailed(109072647)
