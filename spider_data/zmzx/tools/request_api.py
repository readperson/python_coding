import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from tools.time_treatment import now_time
import time


def request_api(url, data):
    print("Push_Date:", now_time())
    print("Data(json):", str(data).replace("'", '"'))
    url = "http://47.97.79.60" + url
    data = json.dumps(data)
    headers = {"Content-Type": "application/json;charset=utf-8"}
    print("Url:", url)
    print("Headers:", headers)
    time.sleep(0.2)
    result = requests.post(url=url, headers=headers, data=data)
    print("Response(Data):", result.text)
    result = json.loads(result.text)
    result_code = int(result["code"])
    if result_code != 0:
        errors = "../tools/errors.txt"
        # errors = "/opt/data_captureAPP/zmzx/tools/errors.txt"
        with open(errors, "a+", encoding="utf-8") as f:
            f.write("Push_Date:" + str(now_time()) + "\n")
            f.write("Data(json)：" + str(data) + "\n")
            f.write("Url:" + str(url) + "\n")
            f.write("Response(Data)" + str(result) + "\n")
            x_count = int(len(str(result)))
            f.write("*" * x_count + "\n")
            f.write("*" * x_count + "\n")
            f.write("*" * x_count + "\n")
        print("|", "".ljust(50, "*"), "|")
        print("|", "WRONG".center(50, "*"), "|")
        print("|", "".rjust(50, "*"), "|")
    print("")
