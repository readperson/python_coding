import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from lxml import etree


def cd_app_data(random, page, cat_id, region_id, city_id):
    url = "http://www.quyundong.com/index/businesslist?random=" + str(random) + "&page=" + str(page) + "&cat_id=" + str(
        cat_id) + "&region_id=" + str(region_id)
    headers = {
        "cookie": "city_id = " + str(city_id)}
    print("cd_app_data", url)
    session = requests.session()
    response = session.get(url=url, headers=headers)
    return response.text


def chang_ci_update():
    try:
        with open("../tools/new_json_code.json", "r", encoding="utf-8") as f:
            json_city = f.read()
            json_city = json.loads(json_city)
            for i in range(int(len(json_city))):
                with open("../tools/pull_failed_update_week.txt", "r", encoding="utf-8")as f2:
                    line = f2.readline()
                    if int(len(line)) > 0:
                        i = int(line)
                        # print("pull_failed_files:======================", i)
                        with open("../tools/pull_failed_update_week.txt", "w", encoding="utf-8") as f1:
                            f1.write("")
                city_id = json_city[i]["city_id"]
                j = 1
                for k in range(int(len(json_city[i]["regions"])) - 1):
                    if "region_id" in json_city[i]["regions"][j]:
                        region_id = json_city[i]["regions"][j]["region_id"]
                    else:
                        region_id = json_city[i]["regions"][j].setdefault('region_id')
                    j = j + 1

                    # print("    ", region_id, one_code, city_name, region_name, two_code)
                    #  拉取第一次获取总页数
                    #  http://www.quyundong.com/index/businesslist?random=0.2852704610714779&page=1&cat_id=1&region_id=693
                    # 参数说明 page 页数 cat_id 球类型 region_id 市下面的区县
                    # 1 羽毛球或者不给值 ,11 足球, 13 篮球, 12 网球, 31游泳, 6乒乓球, 26跆拳道
                    cat_ids = [1, 11, 13, 12]
                    random = 0.2852704610714779

                    # 处理拉取场地信息
                    for cat_id in range(int(len(cat_ids))):
                        data = {"account": "17318203546", "password": "123456"}
                        session = requests.session()
                        post_obj = session.post("http://47.114.6.60/user/login", data)
                        post_obj = post_obj.text
                        post_obj = json.loads(post_obj)
                        access = post_obj["data"]["val"]["access"]
                        cat_id = cat_ids[cat_id]
                        page_num = 1
                        response = cd_app_data(random, page_num, cat_id, region_id, city_id)
                        response = json.loads(response)
                        # 获取页数
                        pages = response["data"]["pages"]
                        # 循环页数
                        for page in range(int(pages)):
                            response = cd_app_data(random, page + 1, cat_id, region_id, city_id)
                            response = json.loads(response)
                            # 组装基本信息数据
                            for c in range(int(len(response["data"]["data"]))):
                                # 场地ID
                                business_id = response["data"]["data"][c]["business_id"]
                                detailed = detailed_handle(business_id, city_id, str(cat_id))
                                print("组装json：", detailed)
                                comm_url = "http://47.114.6.60/playground/save_week_scheduled"
                                week_update_json = json.dumps(detailed)
                                comm_headers = {"Content-Type": "application/json;charset=utf-8",
                                                "Authorization": "Bearer " + access}
                                print("请求url:", comm_url)
                                print("请求头:", comm_headers)
                                print("请求数据:", week_update_json)
                                print("")
    except Exception as e:
        with open("../tools/pull_failed_update_week.txt", "w", encoding="utf-8") as f1:
            string = (str(i))
            f1.write(string)
        print(e)


def detailed_handle(business_id, city_id, cat_id):
    url = "http://www.quyundong.com/detail/" + str(business_id) + "-" + str(cat_id) + ".html"
    headers = {
        "Referer": "http://www.quyundong.com/?city_id =" + str(city_id),
        "Cookie": "Hm_lvt_61bbb43816781eed0951e867c24051dc=1603677658,1603763336,1603845633,1603933628; city_id=" + str(
            city_id) + ";  is_login=0; Hm_lpvt_61bbb43816781eed0951e867c24051dc=1603934942"
    }
    print("detail_url:", url)
    # 定义集合放入数据
    area_info = {}
    area_info["business_id"] = business_id
    response = requests.get(url=url, headers=headers)
    html_detailed_str = response.content.decode("utf-8")
    html = etree.HTML(html_detailed_str)
    weeks = {}
    venuereservation_count_date = html.xpath("count(/html/body/div[3]/form/div[1]/ul/li)")
    for j in range(int(venuereservation_count_date) - 1):
        week = []
        date_time = html.xpath("/html/body/div[3]/form/div[1]/ul/li[" + str(j + 2) + "]/a/@data-time")
        date_time_text = html.xpath("/html/body/div[3]/form/div[1]/ul/li[" + str(j + 2) + "]/a/text()")
        date_time_str = str(date_time[0])
        date_time_text_str = str(date_time_text[0])
        week.append(date_time_text_str)
        week.append(date_time_str)
        url = "http://www.quyundong.com/detail/" + str(business_id) + "-" + str(cat_id) + ".html?t=" + date_time_str
        print("detail_url2", url)
        headers = {
            "Referer": "http://www.quyundong.com/detail/22951-1.html?t=" + date_time_str}
        # 场地编号  1号场   # 2号场    # 3号场    # 4号场    # 5号场    # 6号场   # 7号场  # 8号场  # 9单打  # 10单打
        # 场地编号显示一周的
        response = requests.get(url=url, headers=headers)
        html_detailed_str = response.content.decode("utf-8")
        html_cd = etree.HTML(html_detailed_str)
        area_select = html_cd.xpath("count(/html/body/div[3]/form/div[3]/div[1]/table/tbody/tr)")
        for m in range(int(area_select)):
            area_select_jt = html_cd.xpath(
                "count(/html/body/div[3]/form/div[3]/div[1]/table/tbody/tr[" + str(m + 1) + "]/td)")
            for a in range(int(area_select_jt)):
                court_name = str(html_cd.xpath(
                    "/html/body/div[3]/form/div[3]/div[1]/table/tbody/tr[" + str(m + 1) + "]/td[" + str(
                        a + 1) + "]/@court_name")).replace("['", "").replace("']", "")
                status = str(html_cd.xpath(
                    "/html/body/div[3]/form/div[3]/div[1]/table/tbody/tr[" + str(m + 1) + "]/td[" + str(
                        a + 1) + "]/@status")).replace("['", "").replace("']", "")

                goods_id = str(html_cd.xpath(
                    "/html/body/div[3]/form/div[3]/div[1]/table/tbody/tr[" + str(m + 1) + "]/td[" + str(
                        a + 1) + "]/@goods_id")).replace("['", "").replace("']", "").split(",")[1]
                price = str(html_cd.xpath(
                    "/html/body/div[3]/form/div[3]/div[1]/table/tbody/tr[" + str(m + 1) + "]/td[" + str(
                        a + 1) + "]/@price"))

                week.append(goods_id)
                week.append(court_name)
                week.append(status)
                week.append(price)
        weeks["weeks" + str(j)] = week
    area_info["weeks_list"] = weeks
    return area_info


if __name__ == '__main__':
    chang_ci_update()
