from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.response_api import response_api


def taiesport_zhixunzhongxin():
    url = "https://lol.taiesport.com/OfficialWebsite/news"
    html_page = xpath_html_page(url)
    div_count = xpath_html_count(html_page, "//div[@class='ty_news_list clearBoth']")
    print(div_count)
    for div_c in range(div_count):
        div_texts = xpath_html_value(html_page,
                                     "//div[@class='ty_news_list clearBoth'][" + str(div_c + 1) + "]//text()")
        href = xpath_html_value(html_page,
                                "//div[@class='ty_news_list clearBoth'][" + str(div_c + 1) + "]/a/@href")
        pkey = str(href[0]).split("=")[1]
        div_list = []
        div_list.append(pkey)
        for div_text in div_texts:
            div_t = str(div_text).replace("\n", "").strip(" ")
            if int(len(div_t)) != 0 and div_t != "资讯":
                div_list.append(div_t)
        # /OfficialWebsite/newsDetail?news_id=5362
        # https://lol.taiesport.com/OfficialWebsite/newsDetail?news_id=5362
        div_list.append("https://lol.taiesport.com" + str(href[0]))
        response_api("/ydj/save_zixunzhongxin", div_list)


if __name__ == '__main__':
    taiesport_zhixunzhongxin()
