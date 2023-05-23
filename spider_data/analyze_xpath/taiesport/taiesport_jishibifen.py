from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.response_api import response_api

def taiesport_jishibifen():
    url = "http://data.taiesport.com/data/dota/matchList?op=2"
    html_page = xpath_html_page(url)
    div_count = xpath_html_count(html_page, "//div[@class='inmatch_info_item']")
    for div_c in range(div_count):
        # //div[@class='inmatch_info_item'][1]/div[@class='inmatch_info_list']
        div_count_2 = xpath_html_count(html_page,
                                       "//div[@class='inmatch_info_item'][" + str(
                                           div_c + 1) + "]/div[@class='inmatch_info_list']")
        for dic_c2 in range(div_count_2):
            div_tests = xpath_html_value(html_page, "//div[@class='inmatch_info_item'][" + str(
                div_c + 1) + "]/div[@class='inmatch_info_list'][" + str(dic_c2 + 1) + "]//text()")
            id = xpath_html_value(html_page, "//div[@class='inmatch_info_item'][" + str(
                div_c + 1) + "]/div[@class='inmatch_info_list'][" + str(dic_c2 + 1) + "]/@onclick")
            pkey = str(id[0]).split(",")[1].replace("'", "")
            # print(div_tests)
            div_list = []
            div_list.append(pkey)
            for div_text in div_tests:
                div_t = str(div_text).replace("\n", "").strip(" ")
                if int(len(div_t)) != 0 and div_t != "分析":
                    div_list.append(div_t)

            url = "http://data.taiesport.com/data/dota/MatchDetail?op=1&match_id=" + str(pkey) + "&gid=2"
            div_list.append(url)
            response_api("/ydj/save_jishibifen",div_list)


if __name__ == '__main__':
    taiesport_jishibifen()
