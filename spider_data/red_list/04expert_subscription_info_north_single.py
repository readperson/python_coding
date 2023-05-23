import requests
import json
from tools.red_list.expert_subscription_info import expert_subscription_info
from tools.red_list.inserDBpersonRedTypeList import inserDBpersonRedTypeList


# 北单
def expert_subscription_info_north_single():
    url = "http://cpapi.donggeqiu.com/api/zjtj.action"
    with open("04expert_subscription_info_north_single.txt", "r", encoding="utf-8") as f:
        # historyPlanList
        data_str = f.readlines()
        data_count = int(len(data_str))
        line = 1
        for i in range(data_count):
            print("读取到第", line, "行")
            line = line + 1
            data = data_str[i]
            print(data)
            headers = {"model": "SM-A7070",
                       "newVersion": "android_10.6",
                       "clientType": "donggeqiu",
                       "version": "",
                       "classCode": "000",
                       "source": "72",
                       "sid": "27003100088",
                       "androidId": "bad84b3b9bc4edc2",
                       "Content-Type": "application/x-www-form-urlencoded",
                       "Host": "cpapi.donggeqiu.com",
                       "Connection": "close",
                       "Accept-Encoding": "gzip, deflate",
                       "User-Agent": "okhttp/3.4.1"}
            data = data
            result = requests.post(url=url, headers=headers, data=data)
            result.encoding = "utf-8"
            print(result.text)
            result = json.loads(result.text)
            red_list_type = "北单"
            uid = result["result"]["expertBaseInfo"]["expertsName"]
            name = result["result"]["expertBaseInfo"]["expertsNickName"]
            red_info_north_single = expert_subscription_info(result, red_list_type,"historyPlanList")
            print("json", str(red_info_north_single).replace("'", '"'))
            inserDBpersonRedTypeList(uid, name, red_list_type, str(red_info_north_single).replace("'", '"'))


if __name__ == '__main__':
    expert_subscription_info_north_single()
