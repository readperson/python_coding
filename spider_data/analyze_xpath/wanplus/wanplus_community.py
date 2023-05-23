from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.response_api import response_api


def wanplus_community():
    url = "https://www.wanplus.com/lol/club"
    html_page = xpath_html_page(url)
    li_count = xpath_html_count(html_page, "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/ul/li")

    for li_c in range(li_count):
        community_list = []
        href = xpath_html_value(html_page, "//li[" + str(li_c + 1) + "]/div[@class='com-munber-text']/a/@href")
        pkey = str(href[0]).split("/")[2].split(".")[0]
        community_list.append(pkey)
        li_texts = xpath_html_value(html_page, "//li[" + str(li_c + 1) + "]/div[@class='com-munber-text']//text()")
        for li_text in li_texts:
            li_t = str(li_text).replace("\r\n", "").replace("\xa0", "").replace("\u200b", "").strip(" ")
            if int(len(li_t)) != 0:
                community_list.append(li_t)
        community_list.append("http://www.wanplus.com" + href[0])
        response_api("/wjdj/save_shequ", community_list)


if __name__ == '__main__':
    wanplus_community()
