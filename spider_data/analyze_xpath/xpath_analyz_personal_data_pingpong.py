from tools.xpath_html_analyze_tools.xpath_html_analyze import write_html_backward_climb
from tools.xpath_html_analyze_tools.xpath_html_analyze import red_html
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.base64_text import text_conversion_base64
from tools.response_api import response_api
from tools.random_number import random_number
from tools.random_number import random_city
from tools.random_number import random_year


def pesonal_data_pingpong():
    # url = "http://www.zyypp.com/case/jltd7e3/"
    # html_name = "jltd7e3"
    # file_name = write_html(url, html_name)
    html = red_html("./html_file/jltd7e3.html")
    page_count = xpath_html_count(html, "//ul[@class='case_list clearfix']/li")
    # print(page_count)
    for page in range(page_count):
        base = {}
        page_text = xpath_html_value(html,
                                     "//ul[@class='case_list clearfix']/li[" + str(page + 1) + "]/h3//text()")
        href = xpath_html_value(html,
                                "//ul[@class='case_list clearfix']/li[" + str(page + 1) + "]/a/@href")
        img = xpath_html_value(html,
                               "//ul[@class='case_list clearfix']/li[" + str(page + 1) + "]/a/img/@src")
        # print(href[0])
        # print(str(href[0]).split("/")[4].split(".")[0])
        base["pkey"] = str(href[0]).split("/")[4].split(".")[0]
        base["name"] = page_text[0]
        base["img"] = img[0]
        base["type"] = "乒乓球"
        base["year"] = random_year()
        base["city"] = random_city()
        base["ball_number"] = random_number()
        base["follow_number"] = random_number()
        base["he_follow"] = random_number()
        base["warfare_number"] = random_number()
        html_name_detail = write_html_backward_climb(href[0], base["pkey"])
        html__detail = red_html(html_name_detail)
        # //div[@class='content tab-content']/p
        page_count_detail = xpath_html_count(html__detail, "//div[@class='content tab-content']/p")
        # print(page_count_detail)
        if page_count_detail < 5:
            print("详细介绍小于", page_count_detail, "放弃！")
            continue
        # print(page_count_detail)
        base_list = []
        for pc_de in range(page_count_detail):
            text = str(xpath_html_value(html__detail,
                                        "//div[@class='content tab-content']/p[" + str(pc_de) + "]//text()")).replace(
                "['", "").replace("']", "").replace("[", "").replace("]", "")
            if int(len(text)) > 0:
                base_list.append(text_conversion_base64(text))
        base["detail"] = base_list
        print(base)
        response_api("/football/save_jiaolian", base)


if __name__ == '__main__':
    pesonal_data_pingpong()
