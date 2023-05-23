from tools.xpath_html_analyze_tools.xpath_html_analyze import write_html_backward_climb
from tools.xpath_html_analyze_tools.xpath_html_analyze import red_html
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.base64_text import text_conversion_base64
from tools.response_api import response_api
from tools.random_number import random_number
from tools.random_number import random_city
from tools.random_number import random_year


def personal_data_football():
    for page in range(2):
        url = "http://www.12maty.com/12maty/products/21118320_0_0_" + str(page + 1) + ".html"
        html = xpath_html_page(url)
        html_count = xpath_html_count(html, "//ul[@class='q']/li")
        # print(html_count)
        base = {}
        for h_count in range(html_count):
            href = xpath_html_value(html, "//ul[@class='q']/li[" + str(h_count + 1) + "]/div/a/@href")
            id = str(href[0]).split("/")[3].split(".")[0]
            name = xpath_html_value(html, "//ul[@class='q']/li[" + str(h_count + 1) + "]/div/div/h3//text()")[1]
            img = xpath_html_value(html, "//ul/li[" + str(h_count + 1) + "]//img/@src")
            base["pkey"] = id
            base["name"] = name
            print(name)
            base["img"] = str(img[0]).split("?")[0]
            base["type"] = "足球"
            base["year"] = random_year()
            base["city"] = random_city()
            base["ball_number"] = random_number()
            base["follow_number"] = random_number()
            base["he_follow"] = random_number()
            base["warfare_number"] = random_number()
            html_detial = xpath_html_page("http://www.12maty.com" + str(href[0]))
            html_detial_list = []
            html_detial_div = xpath_html_count(html_detial,
                                               "//div[@class='show-details-article editor_content_air']/div")

            for h_div in range(html_detial_div):
                div_text = xpath_html_value(html_detial,
                                            "//div[@class='show-details-article editor_content_air']/div[" + str(
                                                h_div + 1) + "]//text()")
                for d_t in div_text:
                    if int(len(str(d_t))) > 0:
                        html_detial_list.append(text_conversion_base64(d_t))

            html_detial_p = xpath_html_count(html_detial,
                                             "//div[@class='show-details-article editor_content_air']/p")

            for h_p in range(html_detial_p):
                p_text = xpath_html_value(html_detial,
                                          "//div[@class='show-details-article editor_content_air']/p[" + str(
                                              h_p + 1) + "]//text()")
                p_value_text = ""
                if int(len(p_text)) > 1:
                    for p_t in p_text:
                        # print("pt ----", p_t)
                        pt = str(p_t).replace(" ", "")
                        if int(len(pt)) > 1:
                            p_value_text += p_t
                    html_detial_list.append(text_conversion_base64(p_value_text))

                if int(len(p_text)) == 1:
                    pte = str(p_text[0]).strip()
                    if int(len(pte)) > 0:
                        html_detial_list.append(text_conversion_base64(p_text[0]))

            base["detail"] = html_detial_list
            if int(len(base["detail"])) < 4:
                print("明细数据小于", len(base["detail"]), "放弃")
                print()
                continue
            print(base["detail"])
            print(base)
            # response_api("/football/save_jiaolian", base)


if __name__ == '__main__':
    personal_data_football()
