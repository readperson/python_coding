from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.handl_specialcharacters import chinese_character
from tools.base64_text import text_conversion_base64
from tools.response_api import response_api
import random


# 新闻中心 最新推荐
def xpath_analyze():
    # 重庆青少年  重庆
    url = "http://www.12maty.com/12maty/vip_doc/21118296_3679996_0_1.html"
    html = xpath_html_page(url)
    page_count = xpath_html_count(html, "//a[@class='page-noitem']") + 1
    img_list = []
    for page in range(page_count):
        page += 1
        url_page = "http://www.12maty.com/12maty/vip_doc/21118296_3679996_0_" + str(page) + ".html"
        html_page = xpath_html_page(url_page)
        li_count = xpath_html_count(html_page, '//*[@id="Mo_27"]/table[3]/tbody/tr/td[2]/div/div[1]/ul/li')
        for li_c in range(li_count):
            base = {}
            li_c += 1
            title = chinese_character(
                str(xpath_html_value(html_page, "//li[" + str(li_c) + "]//h3[@class='pic-title']/a/text()"))).replace(
                "重庆", "")
            href = str(xpath_html_value(html_page, "//li[" + str(li_c) + "]//h3[@class='pic-title']/a/@href")[0])
            id = href.split("/")[3].split(".")[0]
            sub_title = str(
                xpath_html_value(html_page, "//li[" + str(li_c) + "]//div[@class='pic-intro']/p/text()")[0]).replace(
                "重庆", "")
            base["pkey"] = id
            base["title"] = text_conversion_base64(title)
            base["sub_title"] = text_conversion_base64(sub_title)
            url_detailed = "http://www.12maty.com" + href
            html_detailed = xpath_html_page(url_detailed)
            detailed_p_count = xpath_html_count(html_detailed, "//div[@class='wap-add-img']/p")
            detailed_list = []
            img_int = 0
            for d_count in range(detailed_p_count):
                d_count += 1
                img_count = xpath_html_count(html_detailed, "//div[@class='wap-add-img']/p[" + str(d_count) + "]/img")
                if img_count == 1:
                    img_text = str(xpath_html_value(html_detailed,
                                                    "//div[@class='wap-add-img']/p[" + str(d_count) + "]/img/@src")[0])
                    img_list.append(img_text)
                    img_int = 1
                    detailed_list.append(text_conversion_base64(img_text))

                text_value = xpath_html_value(html_detailed,
                                              "//div[@class='wap-add-img']/p[" + str(d_count) + "]//text()")
                if int(len(text_value)) == 2:
                    text_value = str(text_value[0] + text_value[1]).replace("重庆", "")
                    detailed_list.append(text_conversion_base64(text_value))
                if int(len(text_value)) == 1:
                    text_value = str(text_value[0]).replace("重庆", "")
                    detailed_list.append(text_conversion_base64(text_value))
            if img_int == 0:
                random_img = random.randint(0, int(len(img_list)) - 1)
                detailed_list.append(text_conversion_base64(img_list[random_img]))

            base["detailed"] = detailed_list
            # python_loging("base" + str(base))
            response_api("/football/save_xunlian", base)
            # python_loging("none")
            # print("base", base)


if __name__ == '__main__':
    xpath_analyze()
