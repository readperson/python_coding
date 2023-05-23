from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.response_api import response_api

# http://www.wanplus.com/dota2/skill/hero
def wanlpus_hero():
    url = "http://www.wanplus.com/dota2/skill/hero"
    html_page = xpath_html_page(url)
    tr_count = xpath_html_count(html_page, "/html/body/div[1]/div[3]/div[3]/table/tbody/tr")
    for tr_c in range(tr_count):
        td_text = xpath_html_value(html_page,
                                   "/html/body/div[1]/div[3]/div[3]/table/tbody/tr[" + str(tr_c + 1) + "]/td//text()")
        hero_list = []
        herf = xpath_html_value(html_page,
                                "/html/body/div[1]/div[3]/div[3]/table/tbody/tr[" + str(tr_c + 1) + "]/td[1]/a/@href")
        id = str(herf[0]).split("/")[3]
        hero_list.append(id)
        imgage = xpath_html_value(html_page,
                                  "/html/body/div[1]/div[3]/div[3]/table/tbody/tr[" + str(
                                      tr_c + 1) + "]/td[1]/a/img/@src")
        hero_list.append(imgage[0])

        for t_text in td_text:
            text = str(t_text).replace("\r\n", "").strip(" ")
            if int(len(text)) != 0:
                hero_list.append(text)
        hero_list.append("http://www.wanplus.com/dota2/hero/" + id)
        response_api("/wjdj/save_yingxiongbang",hero_list)
        print(hero_list)


if __name__ == '__main__':
    wanlpus_hero()
