from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.response_api import response_api


def wanlpus_data():
    url = "https://www.wanplus.com/lol/teamstats"
    html_page = xpath_html_page(url)
    tr_count = xpath_html_count(html_page, "//tbody/tr")
    print(tr_count)
    for tr_c in range(tr_count):
        td_text = xpath_html_value(html_page, "//tbody/tr[" + str(tr_c + 1) + "]/td//text()")
        href = xpath_html_value(html_page, "//tbody/tr[" + str(tr_c + 1) + "]/td[2]/a/@href")
        id = str(href[0]).split("/")[3]
        base_list = []
        base_list.append(id)
        for t_text in td_text:
            base_list.append(t_text)

        # https://www.wanplus.com/lol/team/208
        # headers = {
        #     "Host": "www.wanplus.com",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        #     "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Connection": "close",
        #     "Cookie": "wanplus_token=9da8f2be7a2aba5e424bf2d10005423a; wanplus_storage=lf4m67eka3o; wanplus_sid=6e3c47bf2626c940c57d3f8cb0cf6257; wanplus_csrf=_csrf_tk_313965077; UM_distinctid=1773753f8ca47-0788001b72022a-1a347540-1fa400-1773753f8cb3a; CNZZDATA1275078652=183608789-1611537464-%7C1611564501; wp_pvid=5560123929; wp_info=ssid=s1044778116; Hm_lvt_f69cb5ec253c6012b2aa449fb925c1c2=1611540987; Hm_lpvt_f69cb5ec253c6012b2aa449fb925c1c2=1611569873; isShown=1; gameType=7",
        #     "Upgrade-Insecure-Requests": "1",
        #     "Cache-Control": "max-age=0"
        # }
        url_detail = "https://www.wanplus.com" + str(href[0])
        # detail_list = []
        # print(url_detail)
        html_detail = xpath_html_page(url_detail)

        picture = xpath_html_value(html_detail, "//*[@id='sharePic']/@src")
        base_list.append(picture[0])
        detail_td_1 = xpath_html_value(html_detail, "//*[@class='f15']//text()")
        for td_1 in detail_td_1:
            td = str(td_1).replace("\r\n", "").strip(" ")
            if int(len(td)) != 0:
                base_list.append(td)

        detail_td_2 = xpath_html_value(html_detail,
                                       "//*[@class='team_tbb_te ml10']//text()")
        for td_2 in detail_td_2:
            td2 = str(td_2).replace("\r\n", "").strip(" ")
            if int(len(td2)) != 0:
                base_list.append(td2)
        detail_td_3 = xpath_html_value(html_detail,
                                       "//*[@class='team_tbb_te ml10']/following-sibling::*//text()")
        for td_3 in detail_td_3:
            td3 = str(td_3).replace("\r\n", "").strip(" ")
            if int(len(td3)) != 0:
                base_list.append(td3)
        base_list.append(url_detail)
        response_api("/wjdj/save_shujuku", base_list)

        # base_list.append(detail_list)
        # print(base_list)


if __name__ == '__main__':
    wanlpus_data()
