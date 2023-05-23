import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
import datetime
from lxml import etree
import random
from tools.response_api import response_api
from site_data_capture_all.match import matchId_fun


def cd_app_data(random, page, cat_id, region_id, city_id):
    url = "http://www.quyundong.com/index/businesslist?random=" + str(random) + "&page=" + str(page) + "&cat_id=" + str(
        cat_id) + "&region_id=" + str(region_id)
    headers = {
        "cookie": "city_id = " + str(city_id)}
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
                    # cat_ids = [1, 11, 13, 12]
                    cat_ids = [11]
                    randoms = 0.2852704610714779
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
                        response = cd_app_data(randoms, page_mun, cat_id, region_id, city_id)
                        # ["data"]["pages"]
                        response = json.loads(response)

                        # print(type(response))
                        # 获取页数
                        pages = response["data"]["pages"]
                        # 循环页数
                        for page in range(int(pages)):
                            response = cd_app_data(randoms, page + 1, cat_id, region_id, city_id)
                            response = json.loads(response)
                            # 组装基本信息数据
                            # print(response["data"]["data"])
                            # print(len(response["data"]["data"]))

                            for c in range(int(len(response["data"]["data"]))):
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
                                base["match_time"] = (
                                        datetime.datetime.now() + datetime.timedelta(
                                    days=random.randint(-3, 5))).strftime(
                                    "%Y-%m-%d %H:%M:%S")
                                base["match_type"] = "足球"
                                vacancy_list = [["中锋", "左边锋", "前卫"], ["中锋", "前卫"], ["左边锋", "前卫"], ["左边锋"], ["前卫"]]
                                # 甲
                                base["A_vacancy"] = vacancy_list[random.randint(0, 4)]

                                # 乙
                                base["B_vacancy"] = vacancy_list[random.randint(1, 3)]

                                scale_list = ["3v3", "5v5", "7v7", "11v11"]
                                scale_index = random.randint(0, int(len(scale_list)) - 1)
                                if scale_index == 0:
                                    base["people_number1"] = random.randint(6, 12)
                                    base["people_number2"] = random.randint(12, 18)
                                if scale_index == 1:
                                    base["people_number1"] = random.randint(10, 16)
                                    base["people_number2"] = random.randint(16, 22)
                                if scale_index == 2:
                                    base["people_number1"] = random.randint(14, 20)
                                    base["people_number2"] = random.randint(21, 27)
                                if scale_index == 3:
                                    base["people_number1"] = random.randint(22, 28)
                                    base["people_number2"] = random.randint(29, 35)
                                base["scale"] = scale_list[scale_index]

                                # property
                                property_list = ["对抗赛", "专业对抗赛", "友谊赛"]
                                base["property"] = property_list[random.randint(0, int(len(property_list)) - 1)]
                                # select * from lyc_mingdan where registerInfo_a is not null and registerInfo_b is not null and
                                # unRegisterInfo_a is not null and unRegisterInfo_b is not null
                                # http://47.97.79.60/lyc/mingdan_detail
                                base["matchId"] = matchId_fun()

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

                                # print("area_list", area_list)
                                # print("--------", business_id, name, latitude, longitude, category_id, price, region_id,
                                #       icon_url_pc)

                                # print("detailed", detailed)
                                # 开始组装
                                base["data"] = area_list_data
                                base["detailed"] = detailed_handle(business_id, city_id, cat_id)
                                failed_str = "city_id:" + str(city_id) + ", ctiy_code:" + str(
                                    one_code) + ", city_name:" + city_name + ",  region_id:" + str(
                                    region_id) + ",region_code:" + str(
                                    two_code) + ",region_name:" + region_name + ",cat_id：" + str(
                                    cat_id) + ",page:" + str(
                                    page + 1)
                                print("现在拉取到：", failed_str)
                                print("base", base)
                                response_api("/ygq/save_shangchangshuju", base)


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
    # 定义集合放入数据
    area_info = {}
    # /html/body/div[3]/div[2]/div[2]
    response = requests.get(url=url, headers=headers)
    html_detailed_str = response.content.decode("utf-8")
    html = etree.HTML(html_detailed_str)

    # 电话
    telephone = str(html.xpath("/html/body/div[2]/div[1]/dl/dd[2]/text()")).replace("['", "").replace("']", "")
    area_info["telephone"] = telephone
    count_div = html.xpath("count(/html/body/div[3]/div[2]/div)")
    for i in range(int(count_div)):

        i = i + 1
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
