from tools.requests_api import requests_api
from tools.json_package.json_package import json_package
from tools.response_api import response_api
import time


def show_bill_details(url, headers, data, type):
    show_bill = requests_api(url=url, headers=headers, data=data)
    if show_bill["returndata"]["data"] is not None:

        show_bill_count = int(len(show_bill["returndata"]["data"]))
        for sb_count in range(show_bill_count):
            show_bill_dict = {}
            json_package(show_bill["returndata"]["data"][sb_count], "title", "", show_bill_dict)
            json_package(show_bill["returndata"]["data"][sb_count], "cover", "", show_bill_dict)
            json_package(show_bill["returndata"]["data"][sb_count], "url", "", show_bill_dict)
            json_package(show_bill["returndata"]["data"][sb_count], "isVIP", "", show_bill_dict)
            show_bill_dict["type"] = type
            print("-----------", show_bill_dict)
            chunk_download(show_bill_dict["cover"], show_bill_dict["type"], show_bill_dict["title"])
            url_haibao = "/lyc/save_haibao"
            response_api(url_haibao, show_bill_dict)


def chunk_download(url, types, title):
    import requests
    r = requests.get(url, stream=True)
    time.sleep(0.2)
    with open('./haibao/' + str(types) + '_' + str(time.time()) + '_' + str(title) + '.jpg', 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)
