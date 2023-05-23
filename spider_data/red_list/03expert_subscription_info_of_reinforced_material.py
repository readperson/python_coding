import requests
import json
from tools.red_list.expert_subscription_info import expert_subscription_info
from tools.red_list.inserDBpersonRedTypeList import inserDBpersonRedTypeList


# 北单
def expert_subscription_info_of_reinforced_material():
    url = "http://cpapi.donggeqiu.com/api/zjtj.action"
    with open("03expert_subscription_info_of_reinforced_material.txt", "r", encoding="utf-8") as f:
        # historyPlanList
        data_str = f.readlines()
        data_count = int(len(data_str))
        line = 1
        for i in range(data_count):
            print("读取到第", line, "行")
            line = line + 1
            data = data_str[i]
            print(data)
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = data
            result = requests.post(url=url, headers=headers, data=data)
            result.encoding = "utf-8"
            print(result.text)
            result = json.loads(result.text)
            red_list_type = "北单"
            uid = result["result"]["expertBaseInfo"]["expertsName"]
            name = result["result"]["expertBaseInfo"]["expertsNickName"]
            red_reinforced_material = expert_subscription_info(result, red_list_type, "historyPlanList")

            print("json", str(red_reinforced_material).replace("'", '"'))
            inserDBpersonRedTypeList(uid, name, red_list_type, str(red_reinforced_material).replace("'", '"'))


if __name__ == '__main__':
    expert_subscription_info_of_reinforced_material()
