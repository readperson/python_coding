import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
import datetime
from lxml import etree
from tools.response_api import response_api


def cd_app_data(random, page, cat_id, region_id, city_id):
    url = "http://www.quyundong.com/index/businesslist?random=" + str(random) + "&page=" + str(page) + "&cat_id=" + str(
        cat_id) + "&region_id=" + str(region_id)
    headers = {
        "cookie": "city_id = " + str(city_id)}
    print("cd_app_data:", url, headers)
    session = requests.session()
    response = session.get(url=url, headers=headers)
    return response.text


def code_json_assemble():
    try:
        with open("../tools/new_json_code.json", "r", encoding="utf-8") as f:
            json_city = f.read()
            json_city = json.loads(json_city)
            # print(type(json_city))
            # print("城市json", json_city)
            for i in range(int(len(json_city))):
                with open("../tools/pull_failed_files.txt", "r", encoding="utf-8")as f2:
                    line = f2.readline()
                    if int(len(line)) > 0:
                        i = int(line)

                        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        with open("../tools/pull_failed_files.txt", "w", encoding="utf-8") as f1:
                            f1.write("")
                    city_id = json_city[i]["city_id"]
                    city_name = json_city[i]["city_name"]
                    if "city_code" in json_city[i]:
                        one_code = json_city[i]["city_code"]

                    else:
                        continue
                    # one_code = json_city[i].setdefault("code")
                    # print("-----")

                j = 1
                for k in range(int(len(json_city[i]["regions"])) - 1):
                    if "region_id" in json_city[i]["regions"][j]:
                        region_id = json_city[i]["regions"][j]["region_id"]
                    else:
                        region_id = json_city[i]["regions"][j].setdefault('region_id')

                    region_name = json_city[i]["regions"][j]["region_name"]

                    if "code" in json_city[i]["regions"][j]:
                        two_code = json_city[i]["regions"][j]["code"]
                    else:
                        two_code = json_city[i]["regions"][j].setdefault('code')

                    j = j + 1
                    # print("    ", region_id, one_code, city_name, region_name, two_code)
                    #  拉取第一次获取总页数
                    #  http://www.quyundong.com/index/businesslist?random=0.2852704610714779&page=1&cat_id=1&region_id=693
                    # 参数说明 page 页数 cat_id 球类型 region_id 市下面的区县
                    # 1 羽毛球 ,11 足球, 13 篮球, 12 网球, 6乒乓球,31游泳, 40 健身, 26跆拳道,40 健身
                    # 30 射箭 43武术 42舞蹈 41瑜伽 71篮球计时 69网球人次 67空手道 64武术 40健身 51潜水 38卡丁车  39 热门 桌球35
                    # cat_ids = [1, 11, 13, 12]
                    cat_ids = [30, 43, 42, 41, 71, 69, 67, 64, 40, 51, 38, 39, 35]
                    random = 0.2852704610714779
                    page_mun = 1
                    # cat_id_1 = 1
                    # response = cd_app_data(random, page, cat_id_1, region_id, city_id)
                    # print(response)
                    # # ["data"]["pages"]
                    # response = json.loads(response)
                    # # print(type(response))
                    # # 获取页数
                    # pages = response["data"]["pages"]

                    # 处理拉取场地信息
                    for cat_id in range(int(len(cat_ids))):
                        session = requests.session()
                        data = {"account": "17318203546", "password": "123456"}
                        post_obj = session.post("http://47.114.6.60/user/login", data)
                        post_obj = post_obj.text
                        post_obj = json.loads(post_obj)
                        access = post_obj["data"]["val"]["access"]
                        cat_id = cat_ids[cat_id]
                        response = cd_app_data(random, page_mun, cat_id, region_id, city_id)
                        # ["data"]["pages"]
                        response = json.loads(response)

                        # print(type(response))
                        # 获取页数
                        pages = response["data"]["pages"]
                        # 循环页数
                        for page in range(int(pages)):
                            response = cd_app_data(random, page + 1, cat_id, region_id, city_id)
                            response = json.loads(response)
                            # 组装基本信息数据
                            # print(response["data"]["data"])
                            # print(len(response["data"]["data"]))

                            for c in range(int(len(response["data"]["data"]))):
                                area_list = []
                                base = {}
                                # area = {}
                                area_list_data = {}
                                base["city_id"] = city_id
                                base["city_code"] = one_code
                                base["city_name"] = city_name
                                base["region_id"] = region_id
                                base["region_code"] = two_code
                                base["region_name"] = region_name
                                base["cat_id"] = cat_id
                                base["come_from"] = "趣运动"
                                base["capture_time"] = (
                                        datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime(
                                    "%Y-%m-%d %H:%M:%S")
                                base["capture_type"] = "场地"

                                # 场地ID
                                business_id = response["data"]["data"][c]["business_id"]
                                name = response["data"]["data"][c]["name"]
                                address = response["data"]["data"][c]["address"]
                                first_chart = response["data"]["data"][c]["image_url"]
                                # 经纬度
                                latitude = response["data"]["data"][c]["latitude"]
                                longitude = response["data"]["data"][c]["longitude"]
                                # 场地类型
                                category_id = response["data"]["data"][c]["category_id"]
                                price = response["data"]["data"][c]["price"]
                                # 区县ID
                                region_id = response["data"]["data"][c]["region_id"]
                                # 小图标地址
                                icon_url_pc = response["data"]["data"][c]["icon_url_pc"]
                                # 评分
                                comment_avg = response["data"]["data"][c]["comment_avg"]
                                area_list_data["business_id"] = business_id
                                area_list_data["name"] = name
                                area_list_data["address"] = address
                                area_list_data["first_chart"] = first_chart
                                area_list_data["latitude"] = latitude
                                area_list_data["longitude"] = longitude
                                area_list_data["category_id"] = category_id
                                area_list_data["price"] = price
                                area_list_data["icon_url_pc"] = icon_url_pc
                                area_list_data["comment_avg"] = str(comment_avg)
                                area_list.append(area_list_data)
                                # print("area_list", area_list)
                                # print("--------", business_id, name, latitude, longitude, category_id, price, region_id,
                                #       icon_url_pc)

                                detailed = detailed_handle(business_id, city_id, cat_id)
                                # print("detailed", detailed)
                                # 开始组装
                                base["data"] = area_list
                                base["detailed"] = detailed
                                failed_str = "city_id:" + str(city_id) + ", ctiy_code:" + str(
                                    one_code) + ", city_name:" + city_name + ",  region_id:" + str(
                                    region_id) + ",region_code:" + str(
                                    two_code) + ",region_name:" + region_name + ",cat_id：" + str(
                                    cat_id) + ",page:" + str(
                                    page + 1)
                                print("现在拉取到：", failed_str)
                                response_api("/playground/save_playground", base)
                                # base


    except Exception as e:
        with open("../tools/pull_failed_files.txt", "w", encoding="utf-8") as f1:
            string = (str(i))
            f1.write(string)
        print("=====================================进入异常信息==========================================")
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
    # /html/body/div[3]/div[2]/div[2]
    response = requests.get(url=url, headers=headers)
    html_detailed_str = response.content.decode("utf-8")
    html = etree.HTML(html_detailed_str)

    # 电话
    telephone = str(html.xpath("/html/body/div[2]/div[1]/dl/dd[2]/text()")).replace("['", "").replace("']", "")
    area_info["telephone"] = telephone

    # 温馨提示
    kindly_reminder = str(
        html.xpath("//dd[@class='venuesNotice']/span/text()")).replace("['", "").replace("']", "")

    area_info["kindly_reminder"] = kindly_reminder.replace("\\r\\n", "</br>")
    count_div = html.xpath("count(/html/body/div[3]/div[2]/div)")
    bus_pass_count = 0
    subway_count = 0
    floor_board_count = 0
    lamplight_count = 0
    resting_area_count = 0
    equipment_rental_count = 0
    equipment_maintenance_count = 0
    more_services_count = 0
    bath_facilities_count = 0
    venue_sale_count = 0
    invoice_count = 0
    park_count = 0
    for i in range(int(count_div)):

        i = i + 1
        count_div_c = html.xpath("count(/html/body/div[3]/div[2]/div[" + str(i) + "]/div)")

        for j in range(int(count_div_c + 1)):

            # 交通信息
            text_1 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[1]/text()")
            text_1 = str(text_1).replace("['", "").replace("']", "")

            if text_1 == "公交":
                bus_pass_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                bus_pass = str(text_2).replace("['", "").replace("']", "")
                area_info["bus_pass"] = bus_pass

            if text_1 == "地铁":
                subway_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                subway = str(text_2).replace("['", "").replace("']", "")
                area_info["subway"] = subway

            if text_1 == "地板":
                floor_board_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["floor_board"] = text_2
                # print("------", text_2)

            if text_1 == "灯光":
                lamplight_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["lamplight"] = text_2

            if text_1 == "休息区":
                resting_area_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["resting_area"] = text_2

            if text_1 == "器材租借":
                equipment_rental_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["equipment_rental"] = text_2

            if text_1 == "器材维护":
                equipment_maintenance_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["equipment_maintenance "] = text_2

            if text_1 == "更多服务":
                more_services_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["more_services"] = text_2

            if text_1 == "洗浴设施":
                bath_facilities_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["bath_facilities"] = text_2

            if text_1 == "场馆卖品":
                venue_sale_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["venue_sale"] = text_2

            if text_1 == "发票":
                invoice_count = 1
                text_2 = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["invoice"] = text_2

            if text_1 == "停车":
                park_count = 1
                text_2 = html.xpath(
                    "/html/body/div[3]/div[2]/div[" + str(i) + "]/div[" + str(j) + "]/div[2]/text()")
                text_2 = str(text_2).replace("['", "").replace("']", "")
                area_info["park"] = text_2

        if bus_pass_count == 0:
            area_info["bus_pass"] = ""
        if subway_count == 0:
            area_info["subway"] = ""
        if floor_board_count == 0:
            area_info["floor_board"] = ""
        if lamplight_count == 0:
            area_info["lamplight"] = ""
        if resting_area_count == 0:
            area_info["resting_area"] = ""
        # equipment_rental_count = 0
        if equipment_rental_count == 0:
            area_info["equipment_rental"] = ""
        # equipment_maintenance_count = 0
        if equipment_maintenance_count == 0:
            area_info["equipment_maintenance"] = ""
        # more_services_count = 0
        if more_services_count == 0:
            area_info["more_services"] = ""
        # bath_facilities_count = 0
        if bath_facilities_count == 0:
            area_info["bath_facilities"] = ""
        # venue_sale_count = 0
        if venue_sale_count == 0:
            area_info["venue_sale"] = ""
        # invoice_count = 0
        if invoice_count == 0:
            area_info["invoice"] = ""
        # park_count = 0
        if park_count == 0:
            area_info["park"] = ""
        sx_img = html.xpath("/html/body/div[3]/div[2]/div[" + str(i) + "]/@class")
        sx_img = str(sx_img).replace("['", "").replace("']", "")
        if sx_img == "image":
            img = []
            img_count = html.xpath("count(/html/body/div[3]/div[2]/div[" + str(i) + "]/ul/li)")
            for t in range(int(img_count)):
                # 返回是 单个列表[]
                img_adder = html.xpath(
                    "/html/body/div[3]/div[2]/div[" + str(i) + "]/ul/li[" + str(t + 1) + "]/img/@src")
                img_str = str(img_adder[0])
                img.append(img_str)
            area_info["imgs"] = img

    return area_info


if __name__ == '__main__':
    code_json_assemble()
