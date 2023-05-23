import json
import requests
from tools.get_to_ken import get_to_ken


def area_code_post():
    access = get_to_ken()
    headers = {"Content-Type": "application/json;charset=utf-8",
               "Authorization": "Bearer " + access
               }
    url = "http://47.114.6.60/gps/save_areacode"
    with open("../../tools/new_json_code.json", "r", encoding="utf-8") as f:
        data = f.read()
        data = str(data)
        print(data)
        data = json.loads(data)
        data = json.dumps(data)

        print("url", url)
        print("headers", headers)
        print("data", data)
        rep = requests.post(url=url, data=data, headers=headers)
        print(rep.text)


if __name__ == '__main__':
    area_code_post()
