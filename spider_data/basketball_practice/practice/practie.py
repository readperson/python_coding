from basketball_practice.tools.xpath_url import xpath_count_record_number
from basketball_practice.tools.xpath_url import write_html_page
from basketball_practice.tools.xpath_url import write_html
from basketball_practice.tools.xpath_url import handle_first_dict
from basketball_practice.tools.detail_xpath_handle import detail_xpath_dandle
from basketball_practice.tools.detail_xpath_handle import first_div_list_text
from basketball_practice.tools.detail_xpath_handle import html_content
from tools.response_api import response_api


def practie():
    practie_lists = ["jibendongzuo", "toulan", "1v1", "beida", "yunqiu", "chuanqiu", "lanbanqiu", "xietiaoxing",
                     "xitongxunlian"]
    print(practie_lists.index("jibendongzuo"))
    practie_lists_count = int(len(practie_lists))
    for pli in range(practie_lists_count):
        practie_list = practie_lists[pli]
        url = "http://www.lanqiuhuo.com/" + practie_list + "/"

        html_name = write_html(url, practie_list)
        count_record_frist = "/html/body/div[1]/div/div/div[3]/ul/li"
        page = write_html_page(html_name, count_record_frist)
        if int(page) == 0:
            print("=======只有一页数据的" + practie_list + "==========")
            count_record = "/html/body/div[1]/div/div/div[2]/li"
            count_record_number = xpath_count_record_number(html_name, count_record)
            for c_r_number in range(int(count_record_number)):
                c_r_number += 1
                practie_dict = handle_first_dict(html_name, c_r_number)
                href = "http://www.lanqiuhuo.com" + str(practie_dict["href_a"])
                # print(href)
                practie_dict = handle_first_dict(html_name, c_r_number)
                # print("一页", practie_dict)
                html_file_name = write_html(href, str(practie_dict["id"]))
                # print("详细页面路径 html_file_name", html_file_name)
                html_con = html_content(html_file_name)
                # detail_div_count = xpath_count_record_number(html_file_name,
                #                                              "/html/body/div[1]/div/div/div[2]/div[1]/div")
                # detail_div_count = xpath_count_record_number(html_file_name,
                #                                              ".//div[@class='detail_article']/div")
                # print("每个详细页面div数量 detail_div_count:", detail_div_count)

                # practie_detail = []
                # for d_count in range(detail_div_count):
                #     d_count += 1
                #     detail_xpath_dandle(html_file_name, d_count, practie_detail)
                # practie = first_div_list_text(html_file_name, practie_detail)
                # practie_dict["detail"] = practie
                practie_dict["html_content"] = html_con
                response_api("/basketball/save_lanqiu_xunlian", practie_dict)
                # print("practie_dict", practie_dict)
                # print("")





        else:
            for p in range(int(page)):
                print("=======有多页数据的" + practie_list + "==========")
                # http://www.lanqiuhuo.com/jibendongzuo/list_12_2.html
                # http://www.lanqiuhuo.com/jibendongzuo/list_12_1.html
                for index, value in enumerate(practie_lists):
                    if value == practie_list:
                        url_name = practie_list + "/list_" + str(12 + index) + "_" + str(p + 1) + ".html"
                        url_page = "http://www.lanqiuhuo.com/" + url_name
                        file_name = str(url_name).split(".")[0]
                        # 保存html返回文件名称路径
                        url_result_name = write_html(url_page, str(file_name).replace("/", "-"))
                        # print(url_result_name)
                        # 获取每页的li(记录列表数据)数量
                        count_record_s = "/html/body/div[1]/div/div/div[2]/li"
                        count_record_number = xpath_count_record_number(url_result_name, count_record_s)
                        # print("count_record_number", count_record_number)
                        # base = {}
                        for c_r_number in range(int(count_record_number)):
                            c_r_number += 1
                            practie_dict_page = handle_first_dict(url_result_name, c_r_number)
                            # http://www.lanqiuhuo.com/jibendongzuo/24083.html 详细页面
                            href_page = "http://www.lanqiuhuo.com" + str(practie_dict_page["href_a"])

                            # ../tools/html_file/24083.html 详细页面路径
                            html_file_name_page = write_html(href_page, str(practie_dict_page["id"]))
                            print("详细页面路径 html_file_name_page:", html_file_name_page)
                            html_con_page = html_content(html_file_name_page)

                            # 详细页面div数量  /html/body/div[1]/div/div/div[1]/div[1]/div[7]
                            # detail_div_page_count = xpath_count_record_number(html_file_name_page,
                            #                                                   "/html/body/div[1]/div/div/div[2]/div[1]/div")
                            # detail_div_page_count = xpath_count_record_number(html_file_name_page,
                            # ".//div[@class='detail_article']/div")
                            # print("每个详细页面div数量", detail_div_page_count)
                            # practie_detail_page = []
                            # for d_p_count in range(detail_div_page_count):
                            #     d_p_count += 1
                            #     detail_xpath_dandle(html_file_name_page, d_p_count, practie_detail_page)
                            # practie_page = first_div_list_text(html_file_name_page, practie_detail_page)
                            # practie_dict_page["detail"] = practie_page

                            practie_dict_page["html_content"] = html_con_page
                            response_api("/basketball/save_lanqiu_xunlian", practie_dict_page)
                            # print("practie_dict_page", practie_dict_page)
                            # print("")
                            #
                            # print()


if __name__ == '__main__':
    practie()
