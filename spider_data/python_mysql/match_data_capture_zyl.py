import sys

sys.path.append(r"C:\Users\Administrator\.jenkins\workspace\app_aptrue")
from tools.handl_specialcharacters import hzs_sub
import json
import requests
from lxml import etree
import datetime
import random
import pymysql
import time


def activity_data_capture_zyl():
    try:
        # /html/body/div[1]/div[2]/div/div[10]/ul/li
        url_page = "http://series.zhongyulian.com/exchange/alllist/page/1"
        session_page = requests.session()
        response_page = session_page.get(url_page)
        html_str_page = response_page.content.decode("utf-8")
        html_page = etree.HTML(html_str_page)
        page_count = int(html_page.xpath('count(/html/body/div[1]/div[2]/div/div[10]/ul)'))
        print("page_count", page_count)
        count = 9
        for page in range(count):
            page = page + 1
            print("供", count, "页,正在爬取第", page, "页")
            url = "http://series.zhongyulian.com/exchange/alllist/page/" + str(page)
            # /html/body/div[1]/div[2]/div/div[11]/ul/li
            session = requests.session()
            response = session.get(url)
            html_str = response.content.decode("utf-8")
            html = etree.HTML(html_str)
            div_count = int(html.xpath('count(/html/body/div[1]/div[2]/div/div)'))
            activity_list = []
            for i in range(int(div_count - 1)):
                nowTime = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
                a_href = html.xpath("/html/body/div[1]/div[2]/div/div[" + str(i + 1) + "]/div[1]/a/@href")
                a_href = str(a_href).replace("['", "").replace("']", "")
                ids = a_href.split("/")
                id = ids[int(len(ids)) - 1]
                # print("id", id)
                # id = "5689d0dfc0e88c88268b462a"
                # print("a_href:", a_href)
                # http://series.zhongyulian.com/exchange/info/id/56933db9c0e88cc3058b4be4
                url_info = "http://series.zhongyulian.com" + a_href
                # print("url_info", url_info)
                session = requests.session()
                response = session.get(url_info)
                html_info_str = response.content.decode("utf-8")
                info_html = etree.HTML(html_info_str)
                # /html/body/div[1]/div[1]/div/div[1]/div[1]

                #
                # 图片/html/body/div[1]/div[1]/div/div[1]/div[1]/div/div/a/img
                # 名字/html/body/div[1]/div[1]/div/div[1]/div[1]/div/h3
                # 报名人数 /html/body/div[1]/div[1]/div/div[1]/div[1]/div/a/div/span
                # 比分 /html/body/div[1]/div[1]/div/div[1]/div[2]/h1[2]
                # /html/body/div[1]/div[1]/div/div[1]/div[3]/div/div/a/img
                # /html/body/div[1]/div[1]/div/div[1]/div[3]/div/h3
                # /html/body/div[1]/div[1]/div/div[1]/div[3]/div/a/div/span
                # right
                # middle
                # left
                activity_dict = {}
                right_img = str(
                    info_html.xpath("/html/body/div[1]/div[1]/div/div[1]/div[1]/div/div/a/img/@src")).replace(
                    "['",
                    "").replace(
                    "']", "")
                right_name = str(info_html.xpath("/html/body/div[1]/div[1]/div/div[1]/div[1]/div/h3/text()")).replace(
                    "['",
                    "").replace(
                    "']", "")
                right_press_count = str(
                    info_html.xpath("/html/body/div[1]/div[1]/div/div[1]/div[1]/div/a/div/span/text()")).replace("['",
                                                                                                                 "").replace(
                    "']", "")
                # print(right_img, right_name, right_press_count)
                middle_score = str(info_html.xpath('/html/body/div[1]/div[1]/div/div[1]/div[2]/h1[2]/text()')).replace(
                    "['",
                    "").replace(
                    "']", "").replace("\\xa0-\\xa0", " vs ")
                # print(middle_score)
                left_img = str(
                    info_html.xpath("/html/body/div[1]/div[1]/div/div[1]/div[3]/div/div/a/img/@src")).replace(
                    "['",
                    "").replace(
                    "']", "")
                left_name = str(info_html.xpath("/html/body/div[1]/div[1]/div/div[1]/div[3]/div/h3/text()")).replace(
                    "['",
                    "").replace(
                    "']", "")
                left_press_count = str(
                    info_html.xpath("/html/body/div[1]/div[1]/div/div[1]/div[3]/div/a/div/span/text()")).replace("['",
                                                                                                                 "").replace(
                    "']", "")
                # print(left_img, left_name, left_press_count)
                # 比赛时间 /html/body/div[1]/div[1]/div/div[2]/div[1]/div[2]/h4
                # 比赛地点 /html/body/div[1]/div[1]/div/div[2]/div[1]/div[4]/h4
                # 奖品设置 /html/body/div[1]/div[1]/div/div[2]/div[1]/div[6]/h4
                # match_time = str(info_html.xpath("/html/body/div[1]/div[1]/div/div[2]/div[1]/div[2]/h4/text()")).replace(
                #     "['",
                #     "").replace(
                #     "']", "").replace("\\r\\n", "").replace("\\t", "")
                day = random.randint(0, 8)
                # print("day:", day)
                match_time = (datetime.datetime.now() + datetime.timedelta(days=+day)).strftime(
                    "%Y-%m-%d %H:%M:%S")
                # print("match_time", match_time)
                # print("minTime", minTime)
                # print("match_time",match_time)
                match_address = str(
                    info_html.xpath("/html/body/div[1]/div[1]/div/div[2]/div[1]/div[4]/h4/text()")).replace(
                    "['", "").replace("']", "").replace("\\r\\n", "").replace("\\t", "")
                match_prize = str(
                    info_html.xpath("/html/body/div[1]/div[1]/div/div[2]/div[1]/div[6]/h4/text()")).replace(
                    "['",
                    "").replace(
                    "']", "").replace("\\r\\n", "").replace("\\t", "")

                #
                #  http://series.zhongyulian.com/exchange/info/id/5698794ec0e88c756b8b45f3
                #  对阵列表/html/body/div[1]/div[5]/div
                #
                clasli_count = int(info_html.xpath('count(/html/body/div[1]/div[5]/div)'))
                # print(" clasli_count:", clasli_count)
                if clasli_count == 1:
                    activity_dict["id"] = id
                    activity_dict["come_from"] = "中羽连"
                    activity_dict["capture_data"] = nowTime
                    activity_dict["capture_type"] = "比赛"
                    activity_dict["right_img"] = right_img
                    activity_dict["right_name"] = right_name
                    activity_dict["right_person_count"] = right_press_count
                    activity_dict["middle_score"] = middle_score
                    activity_dict["left_img"] = left_img
                    activity_dict["left_name"] = left_name
                    activity_dict["left_person_count"] = left_press_count
                    activity_dict["match_time"] = match_time
                    activity_dict["match_address"] = match_address
                    activity_dict["match_prize"] = match_prize
                    activity_dict["competitionprogress"] = "即将开战"
                    activity_dict["competition_status"] = "0"

                    db = pymysql.connect("47.97.79.60", "root", "#2020mysql56root", "tyds", charset='utf8')
                    # 使用cursor()方法获取操作游标
                    cursor = db.cursor()
                    sql_query = "SELECT * FROM clasli_base  WHERE id='%s' " % (id)
                    cursor.execute(sql_query)
                    data_query = cursor.rowcount
                    if data_query == 0:
                        activity_dict1 = str(activity_dict).replace("'", '"')
                        print("-------------未开始活动" + id + "-----------------")
                        # SQL 插入语句
                        sql_insert = "INSERT INTO clasli_base (id,come_from,capture_data, capture_type, right_img, right_name," \
                                     "right_person_count,middle_score,left_img,left_name,left_person_count,match_time," \
                                     "match_address,competitionprogress,competition_status,match_prize,activity_json) " \
                                     "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                         id, "中羽连", nowTime, "比赛", right_img, right_name, right_press_count,
                                         middle_score,
                                         left_img,
                                         left_name, left_press_count, match_time, match_address, "即将开战", "0",
                                         match_prize,
                                         activity_dict1)
                        try:
                            # 执行sql语句
                            cursor.execute(sql_insert)
                            # 提交到数据库执行
                            db.commit()
                        except:
                            # Rollback in case there is any error
                            db.rollback()

                        # 关闭数据库连接
                        db.close()
                    else:
                        print(id, "未开始,已存在,update,match_time:", match_time)
                        sql_update = "update clasli_base set match_time='" + match_time + "' where id = '%s'" % (id)
                        cursor.execute(sql_update)
                        # 提交到数据库执行
                        db.commit()
                        # continue
                else:
                    try:
                        activity_dict["id"] = id
                        activity_dict["come_from"] = "中羽连"
                        activity_dict["capture_data"] = nowTime
                        activity_dict["capture_type"] = "比赛"
                        activity_dict["right_img"] = right_img
                        activity_dict["right_name"] = right_name
                        activity_dict["right_person_count"] = right_press_count
                        activity_dict["middle_score"] = middle_score
                        activity_dict["left_img"] = left_img
                        activity_dict["left_name"] = left_name
                        activity_dict["left_person_count"] = left_press_count
                        activity_dict["match_time"] = match_time
                        activity_dict["match_address"] = match_address
                        activity_dict["match_prize"] = match_prize
                        activity_dict["competitionprogress"] = "已经完成"
                        activity_dict["competition_status"] = "1"
                        # 使用cursor()方法获取操作游标
                        db = pymysql.connect("47.97.79.60", "root", "#2020mysql56root", "tyds", charset='utf8')
                        # 使用cursor()方法获取操作游标
                        cursor = db.cursor()
                        sql_query = "SELECT * FROM clasli_base  WHERE id='%s' " % (id)
                        cursor.execute(sql_query)
                        data_query = cursor.rowcount
                        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime(
                            "%Y-%m-%d %H:%M:%S")
                        if data_query == 0:
                            activity_dict2 = str(activity_dict).replace("'", '"')

                            print("-------------插入活动" + id + ":时间" + capture_time + "-----------------")
                            # SQL 插入语句
                            sql_insert = "INSERT INTO clasli_base (id,come_from,capture_data, capture_type, right_img, right_name," \
                                         "right_person_count,middle_score,left_img,left_name,left_person_count,match_time," \
                                         "match_address,competitionprogress,competition_status,match_prize,activity_json) " \
                                         "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                             id, "中羽连", nowTime, "比赛", right_img, right_name, right_press_count,
                                             middle_score, left_img, left_name, left_press_count, match_time,
                                             match_address,
                                             "已经完成", "1", match_prize, activity_dict2)
                            cursor.execute(sql_insert)
                            # db.commit()
                            # 提交到数据库执行

                        else:
                            print(id, "已开始,已存在,update,match_time:", match_time)
                            sql_update = "update clasli_base set match_time='" + match_time + "' where id = '%s'" % (id)
                            cursor.execute(sql_update)
                            # 提交到数据库执行
                            db.commit()
                            continue

                        # /html/body/div[1]/div[5]/div['+str(j)+']/div[
                        clasli_list = []
                        for j in range(clasli_count):
                            j = j + 1
                            j_count = int(info_html.xpath('count(/html/body/div[1]/div[5]/div[' + str(j) + ']/div)'))
                            # print("      j_count:", j_count)
                            # /html/body/div[1]/div[5]/div[1]/div[1]/div/div
                            # /html/body/div[1]/div[5]/div[2]/div[1]/div/div[1]
                            # /html/body/div[1]/div[5]/div[7]/div[1]/div/div[1]/img
                            # /html/body/div[1]/div[5]/div[7]/div[1]/div/div[3]/img
                            k_count = int(info_html.xpath(
                                'count(/html/body/div[1]/div[5]/div[' + str(j) + ']/div[' + str(
                                    j_count) + ']/div/div)'))
                            # print("              k_count:", k_count)

                            #     /html/body/div[1]/div[5]/div[4]/div[1]/div/div/img
                            #     /html/body/div[1]/div[5]/div[5]/div[1]/div/div/img

                            if k_count == 1:
                                clasli_dict1 = {}

                                left_list = []
                                right_list = []
                                left_dict = {}
                                right_dict = {}

                                left_clasli_img = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div/img/@src")
                                left__clasli_name = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div/h5/text()")
                                middle_clasli_score = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[2]/div/h3/text()")
                                middle_clasli_type = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[2]/div/div/span/text()")
                                right_clasli_img = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div/img/@src")
                                right_clasli_name = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div/h5/text()")
                                left_dict["left_clasli_img"] = str(left_clasli_img).replace("['", "").replace("']", "")
                                left_dict["left__clasli_name"] = hzs_sub(
                                    str(left__clasli_name).replace("['", "").replace("']",
                                                                                     "").replace(
                                        "\\r\\n", "").replace("\\t", ""))
                                left_list.append(left_dict)
                                clasli_dict1["middle_clasli_score"] = str(middle_clasli_score).replace("['",
                                                                                                       "").replace(
                                    "']",
                                    "")
                                clasli_dict1["middle_clasli_type"] = str(middle_clasli_type).replace("['", "").replace(
                                    "']",
                                    "")
                                right_dict["right_clasli_img"] = str(right_clasli_img).replace("['", "").replace("']",
                                                                                                                 "")
                                right_dict["right_clasli_name"] = hzs_sub(
                                    str(right_clasli_name).replace("['", "").replace("']",
                                                                                     "").replace(
                                        "']", "").replace("\\r\\n", "").replace("\\t", ""))
                                right_list.append(right_dict)
                                clasli_dict1["left"] = left_list
                                clasli_dict1["right"] = right_list
                                clasli_list.append(clasli_dict1)

                                # print("clasli_dict1", clasli_dict1)
                                # print("clasli_list1", clasli_list)

                            if k_count == 2:
                                clasli_dict2 = {}
                                left_list2 = []
                                right_list2 = []
                                left_dict1 = {}
                                left_dict2 = {}
                                right_dict1 = {}
                                right_dict2 = {}
                                # /html/body/div[1]/div[5]/div[1]/div[1]/div/div[1]/img
                                # /html/body/div[1]/div[5]/div[1]/div[1]/div/div[1]/h5
                                left_clasli_img1 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[1]/img/@src")
                                left_clasli_img1 = str(left_clasli_img1).replace("['", "").replace("']", "")
                                left_clasli_name1 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[1]/h5/text()")
                                left_clasli_name1 = str(left_clasli_name1).replace("['", "").replace("']", "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")

                                # /html/body/div[1]/div[5]/div[1]/div[1]/div/div[2]/img
                                # /html/body/div[1]/div[5]/div[1]/div[1]/div/div[2]/h5
                                left_clasli_img2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[2]/img/@src")
                                left_clasli_img2 = str(left_clasli_img2).replace("['", "").replace("']", "")
                                left_clasli_name2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[2]/h5/text()")
                                left_clasli_name2 = str(left_clasli_name2).replace("['", "").replace("']", "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")

                                # /html/body/div[1]/div[5]/div[1]/div[2]/div/h3
                                # /html/body/div[1]/div[5]/div[1]/div[2]/div/div/span
                                middle_clasli_score2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[2]/div/h3/text()")
                                middle_clasli_score2 = str(middle_clasli_score2).replace("['", "").replace("']", "")
                                middle_clasli_type2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[2]/div/div/span/text()")
                                middle_clasli_type2 = str(middle_clasli_type2).replace("['", "").replace("']", "")

                                # --------------

                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[1]/img
                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[1]/h5
                                right_clasli_img1 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[1]/img/@src")
                                right_clasli_img1 = str(right_clasli_img1).replace("['", "").replace("']", "")
                                right_clasli_name1 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[1]/h5/text()")
                                right_clasli_name1 = str(right_clasli_name1).replace("['", "").replace("']",
                                                                                                       "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")

                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[2]/img
                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[2]/h5
                                right_clasli_img2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[2]/img/@src")
                                right_clasli_img2 = str(right_clasli_img2).replace("['", "").replace("']", "")
                                right_clasli_name2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[2]/h5/text()")
                                right_clasli_name2 = str(right_clasli_name2).replace("['", "").replace("']",
                                                                                                       "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")
                                left_dict1["left_clasli_img"] = left_clasli_img1
                                left_dict1["left_clasli_name"] = hzs_sub(left_clasli_name1)
                                left_list2.append(left_dict1)
                                left_dict2["left_clasli_img"] = left_clasli_img2
                                left_dict2["left_clasli_name"] = hzs_sub(left_clasli_name2)
                                left_list2.append(left_dict2)

                                clasli_dict2["middle_clasli_score"] = middle_clasli_score2
                                clasli_dict2["middle_clasli_type"] = middle_clasli_type2

                                right_dict1["right_clasli_img"] = right_clasli_img1
                                right_dict1["right_clasli_name"] = hzs_sub(right_clasli_name1)
                                right_list2.append(right_dict1)
                                right_dict2["right_clasli_img"] = right_clasli_img2
                                right_dict2["right_clasli_name"] = hzs_sub(right_clasli_name2)
                                right_list2.append(right_dict2)

                                clasli_dict2["left"] = left_list2
                                clasli_dict2["right"] = right_list2
                                # print("clasli_dict2", clasli_dict2)
                                clasli_list.append(clasli_dict2)
                                # print("clasli_list2", clasli_list)
                            # print("right_clasli_list", clasli_list)

                            if k_count == 3:
                                clasli_dict3 = {}
                                left_list3 = []
                                right_list3 = []
                                left_dict1 = {}
                                left_dict2 = {}
                                left_dict3 = {}
                                right_dict1 = {}
                                right_dict2 = {}
                                right_dict3 = {}
                                # /html/body/div[1]/div[5]/div[7]/div[1]/div/div[1]/img
                                # /html/body/div[1]/div[5]/div[1]/div[1]/div/div[1]/img
                                # /html/body/div[1]/div[5]/div[1]/div[1]/div/div[1]/h5
                                left_clasli_img1 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[1]/img/@src")
                                left_clasli_img1 = str(left_clasli_img1).replace("['", "").replace("']", "")
                                right_clasli_name1 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[1]/h5/text()")
                                left_clasli_name1 = str(right_clasli_name1).replace("['", "").replace("']", "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")

                                # /html/body/div[1]/div[5]/div[1]/div[1]/div/div[2]/img
                                # /html/body/div[1]/div[5]/div[1]/div[1]/div/div[2]/h5
                                left_clasli_img2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[2]/img/@src")
                                left_clasli_img2 = str(left_clasli_img2).replace("['", "").replace("']", "")
                                left_clasli_name2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[2]/h5/text()")
                                left_clasli_name2 = str(left_clasli_name2).replace("['", "").replace("']", "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")

                                left_clasli_img3 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[3]/img/@src")
                                left_clasli_img3 = str(left_clasli_img3).replace("['", "").replace("']", "")
                                left_clasli_name3 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[1]/div/div[3]/h5/text()")
                                left_clasli_name3 = str(left_clasli_name3).replace("['", "").replace("']", "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")

                                # /html/body/div[1]/div[5]/div[1]/div[2]/div/h3
                                # /html/body/div[1]/div[5]/div[1]/div[2]/div/div/span
                                # /html/body/div[1]/div[5]/div[7]/div[2]/div/div/span
                                middle_clasli_score3 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[2]/div/h3/text()")
                                middle_clasli_scor3 = str(middle_clasli_score3).replace("['", "").replace("']", "")
                                middle_clasli_type3 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[2]/div/div/span/text()")
                                middle_clasli_type3 = str(middle_clasli_type3).replace("['", "").replace("']", "")

                                # --------------

                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[1]/img
                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[1]/h5
                                right_clasli_img1 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[1]/img/@src")
                                right_clasli_img1 = str(right_clasli_img1).replace("['", "").replace("']", "")
                                right_clasli_name1 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[1]/h5/text()")
                                right_clasli_name1 = str(right_clasli_name1).replace("['", "").replace("']",
                                                                                                       "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")

                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[2]/img
                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[2]/h5
                                right_clasli_img2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[2]/img/@src")
                                right_clasli_img2 = str(right_clasli_img2).replace("['", "").replace("']", "")
                                right_clasli_name2 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[2]/h5/text()")
                                right_clasli_name2 = str(right_clasli_name2).replace("['", "").replace("']",
                                                                                                       "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")

                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[2]/img
                                # /html/body/div[1]/div[5]/div[1]/div[3]/div/div[2]/h5
                                right_clasli_img3 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[3]/img/@src")
                                right_clasli_img3 = str(right_clasli_img3).replace("['", "").replace("']", "")
                                right_clasli_name3 = info_html.xpath(
                                    "/html/body/div[1]/div[5]/div[" + str(j) + "]/div[3]/div/div[3]/h5/text()")
                                right_clasli_name3 = str(right_clasli_name3).replace("['", "").replace("']",
                                                                                                       "").replace(
                                    "\\r\\n",
                                    "").replace(
                                    "\\t", "")
                                left_dict1["left_clasli_img"] = left_clasli_img1
                                left_dict1["left_clasli_name"] = hzs_sub(left_clasli_name1)
                                left_list3.append(left_dict1)
                                left_dict2["left_clasli_img"] = left_clasli_img2
                                left_dict2["left_clasli_name"] = hzs_sub(left_clasli_name2)
                                left_list3.append(left_dict2)
                                left_dict3["left_clasli_img"] = left_clasli_img3
                                left_dict3["left_clasli_name"] = hzs_sub(left_clasli_name3)
                                left_list3.append(left_dict3)

                                clasli_dict3["middle_clasli_score"] = middle_clasli_scor3
                                clasli_dict3["middle_clasli_type"] = middle_clasli_type3

                                right_dict1["right_clasli_img"] = right_clasli_img1
                                right_dict1["right_clasli_name"] = (right_clasli_name1)
                                right_list3.append(right_dict1)
                                right_dict2["right_clasli_img"] = right_clasli_img2
                                right_dict2["right_clasli_name"] = hzs_sub(right_clasli_name2)
                                right_list3.append(right_dict2)
                                right_dict3["right_clasli_img"] = right_clasli_img3
                                right_dict3["right_clasli_name"] = hzs_sub(right_clasli_name3)
                                right_list3.append(right_dict3)

                                clasli_dict3["left"] = left_list3
                                clasli_dict3["right"] = right_list3
                                # print("clasli_dict3", clasli_dict3)
                                clasli_list.append(clasli_dict3)
                                # print("clasli_list3", clasli_list)
                                clasli_list.append(clasli_dict3)

                        activity_dict["clasli_list"] = clasli_list
                        clasli_list = str(clasli_list).replace("'", '"')
                        # print("clasli_list;;;", clasli_list)
                        sql_insert = "INSERT INTO clasli_person_list (rid,clasli_person_json)" \
                                     "VALUES ('%s','%s')" \
                                     % (id, clasli_list)
                        # print("sql_insert",sql_insert)
                        cursor.execute(sql_insert)
                        # db.commit()

                        # 图片  http://series.zhongyulian.com/exchange/allphoto/csid/56933db9c0e88cc3058b4be4/index/2
                        csid = a_href.split("/")
                        # print(len(csid))
                        csid = csid[len(csid) - 1]
                        url_img_info = "http://series.zhongyulian.com/exchange/allphoto/csid/" + str(csid) + "/index/2"
                        session = requests.session()
                        response = session.get(url_img_info)
                        html_img_info_str = response.content.decode("utf-8")
                        info_img_html = etree.HTML(html_img_info_str)

                        match_img_count = int(info_img_html.xpath('count(/html/body/div[1]/div[1]/div)'))
                        if match_img_count == 0:
                            continue
                        # print(match_img_count)
                        clasli_img_list = []
                        for img_count in range(int(match_img_count)):
                            img = info_img_html.xpath("/html/body/div[1]/div[1]/div[" + str(img_count + 1) + "]/@style")
                            img = str(img).split("(")[1].split(")")[0]
                            # print("img", img)

                            clasli_img_list.append(img)

                        sql_insert = "INSERT INTO clasli_img (rid,clasli_img)" \
                                     "VALUES ('%s','%s')" \
                                     % (id, str(clasli_img_list).replace("'", '"'))
                        cursor.execute(sql_insert)

                        db.commit()
                        activity_dict["clasli_img_list"] = clasli_img_list


                    except Exception as e:
                        print(
                            "————————————————————————————插入数据异常,事物已回滚" + capture_time + "————————————————————————————————————")
                        activity_data_capture_zyl()

                        # Rollback in case there is any error
                        db.rollback()
                        print(e)

                    # 关闭数据库连接
                    db.close()

                print("组装成功的json:", str(activity_dict).replace("'", '"'))
                print("")
    except Exception as e1:
        s_time = 30
        print("出现错误", s_time, "秒再次执行")
        time.sleep(s_time)
        print(e1)
        print("")
        activity_data_capture_zyl()


if __name__ == '__main__':
    activity_data_capture_zyl()
