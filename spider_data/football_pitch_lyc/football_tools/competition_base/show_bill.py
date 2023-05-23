import sys

sys.path.append("/opt/data_captureAPP")
from tools.headers_json.headers_json import headers_json
from football_pitch_lyc.football_tools.competition_detailed.show_bill_Details import show_bill_details
import math
from tools.requests_api import requests_api


# 海报
def show_bill():
    # 17 赛事, 18 形象, 23 邀请
    show_bill_lists_type_id = [17, 18, 23]
    type_id_count = int(len(show_bill_lists_type_id))
    for ti_count in range(type_id_count):
        type_id = show_bill_lists_type_id[ti_count]
        url_page = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
        headers = headers_json()
        data_page = 'json={"method":"vendor_jzqx_loadPosterList","type_id":' + str(
            type_id) + ',"style":1,"page":1,"limit":10,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"594eddfa0c1099fb2bd51b04515e1c194ca33c7b"}'
        rep = requests_api(url_page, headers, data_page)
        count = int(rep["returndata"]["count"])

        # count = 247
        page_count = math.ceil(count / 10)
        page = 1
        for p in range(page_count):
            url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
            data = 'json={"method":"vendor_jzqx_loadPosterList","type_id":' + str(type_id) + ',"style":1,"page":' + str(
                page) + ',"limit":10,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"594eddfa0c1099fb2bd51b04515e1c194ca33c7b"}'
            show_bill_details(url, headers, data, type_id)

            page = page + 1



if __name__ == '__main__':
    show_bill()
