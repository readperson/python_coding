import requests
import json
from basketball_practice.basket_ring_qyd.data_handle import data_lens
from basketball_practice.basket_ring_qyd.data_handle import json_data_handle
from tools.response_api import response_api


def basket_ring():
    url_file = "url_file"
    with open(url_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            url = str(line).replace("\n", "").replace('"', '')
            print(url)
            basket_result = requests.get(url=url)
            basket_result = json.loads(basket_result.text)
            data_count = data_lens(basket_result["data"]["list"])
            list_dict = ["id", "coterie_id", "content=base64", "has_attach", "user_id", "is_top",
                         "top_weight", "status", "views", "add_time", "last_update_time",
                         "comment_count", "coterie_name", "user_name", "user_avatar"]

            for d_c in range(data_count):
                json_dict = json_data_handle(basket_result["data"]["list"], d_c, list_dict)
                if str(json_dict["user_name"]).find("趣运动") == 0:
                    continue
                if str(json_dict["user_name"]).find("篮球圈圈主") == 0:
                    continue
                attach_list_count = data_lens(basket_result["data"]["list"][d_c]["attach_list"])
                attach_list_s = ["url", "post_id", "attach_id", "thumb_url"]
                attach_list = []
                for a_l_c in range(attach_list_count):
                    attach_list.append(
                        json_data_handle(basket_result["data"]["list"][d_c]["attach_list"], a_l_c, attach_list_s))
                json_dict["attach_list"] = attach_list
                print("----", json_dict)
                # response_api("/basketball/save_lanqiuquan", json_dict)


if __name__ == '__main__':
    basket_ring()
