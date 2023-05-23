import requests
import json
from tools.red_list.insertBDbase import inserDBpersonList
from tools.base64_text import text_conversion_base64
from tools.random_number import random_number_price_red_list


def expert_subscription():
    url = "http://cpapi.donggeqiu.com/api/zjtj.action"
    with open("expert_subscription.txt", "r", encoding="utf-8") as f:
        data_str = f.readlines()
        data_count = int(len(data_str))
        for i in range(data_count):
            data = data_str[i]
            # print(data)
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = data
            result = requests.post(url=url, headers=headers, data=data).text
            result = json.loads(result)
            print("-------------", result)
            result_count = int(len(result["result"]["data"]))
            # print(result_count)

            for r_count in range(result_count):
                uid = result["result"]["data"][r_count]["EXPERTS_NAME"]
                name = result["result"]["data"][r_count]["EXPERTS_NICK_NAME"]
                # EXPERTS_INTRODUCTION
                EXPERTS_INTRODUCTION = result["result"]["data"][r_count]["EXPERTS_INTRODUCTION"]
                EXPERTS_INTRODUCTION = text_conversion_base64(EXPERTS_INTRODUCTION)
                result["result"]["data"][r_count]["EXPERTS_INTRODUCTION"] = EXPERTS_INTRODUCTION
                result["result"]["data"][r_count]["PRICE"] = str(random_number_price_red_list())
                # base["PRICE"] = str(random_number_price_red_list())
                base = str(result["result"]["data"][r_count]).replace("'", '"')
                print("EXPERTS_NICK_NAME", name)
                print("json:", base)
                inserDBpersonList(uid, name, base)
                # print("")


#


if __name__ == '__main__':
    expert_subscription()
