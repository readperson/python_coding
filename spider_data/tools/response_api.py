import json
import requests
from tools.time_treatment import now_time


def response_api(url, data):
    print("Push_Date:", now_time())
    print("request_json", str(data).replace("'", '"'))
    url = "http://47.97.79.60" + url
    # print(url)
    data = json.dumps(data)
    headers = {"Content-Type": "application/json;charset=utf-8"}
    print("url:", url)
    result = requests.post(url=url, headers=headers, data=data)
    print("响应报文:", result.text)
    result = json.loads(result.text)
    if "code" in result:
        result_code = int(result["code"])
        if result_code != 0:
            print("|", "".ljust(100, "*"), "|")
            print("|", "WRONG!".center(100, "*"), "|")
            print("|", "".rjust(100, "*"), "|")
            print("")
        print("")
    else:
        print("|", "".ljust(100, "*"), "|")
        print("|", "Exception!".center(100, "*"), "|")
        print("|", "".rjust(100, "*"), "|")
        print("")
