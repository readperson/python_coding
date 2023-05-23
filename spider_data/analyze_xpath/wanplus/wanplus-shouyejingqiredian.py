from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.base64_text import text_conversion_base64
from tools.response_api import response_api


def wanplus_shouyejingqiredian():
    url = "http://www.wanplus.com/dota2"
    html_page = xpath_html_page(url)
    # /html/body/div[1]/div[4]/div[3]/div[3]/ul/li
    count_li = xpath_html_count(html_page, "/html/body/div[1]/div[4]/div[3]/div[3]/ul/li")
    print(count_li)
    redian_dict = {}
    for c_li in range(count_li):
        image = xpath_html_value(html_page,
                                 "/html/body/div[1]/div[4]/div[3]/div[3]/ul/li[" + str(c_li + 1) + "]/a/img/@src")
        href = xpath_html_value(html_page,
                                "/html/body/div[1]/div[4]/div[3]/div[3]/ul/li[" + str(c_li + 1) + "]/a/@href")
        id = str(href[0]).split("/")[4].split(".")[0]
        title = xpath_html_value(html_page, "/html/body/div[1]/div[4]/div[3]/div[3]/ul/li[" + str(
            c_li + 1) + "]/div/div/div/a/text()")
        name_day = xpath_html_value(html_page, "/html/body/div[1]/div[4]/div[3]/div[3]/ul/li[" + str(
            c_li + 1) + "]/div/div/p//text()")

        redian_dict["image"] = image[0]
        redian_dict["href"] = href[0]
        redian_dict["title"] = text_conversion_base64(title[0])
        redian_dict["pkey"] = id
        redian_dict["name_day"] = name_day
        detailed_html = xpath_html_page(href[0])
        detailed = xpath_html_value(detailed_html, "/html/body/div[1]/div[2]/div[2]/div[1]//text()")
        # print("----", detailed)
        detailed_list = []
        for detailed_text in detailed:
            d_text = str(detailed_text).replace("\n", "").strip(" ")
            if int(len(d_text)) != 0:
                detailed_list.append(text_conversion_base64(d_text))

        redian_dict["data"] = detailed_list
        response_api("/wjdj/save_jinqiredian", redian_dict)
        # print(redian_dict)


if __name__ == '__main__':
    wanplus_shouyejingqiredian()
