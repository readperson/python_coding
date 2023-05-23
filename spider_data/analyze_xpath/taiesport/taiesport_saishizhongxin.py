from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.response_api import response_api


def taiesport_saishizhongxin():
    url = "http://data.taiesport.com/data/dota/LeagueList"
    html_page = xpath_html_page(url)
    div_count = xpath_html_count(html_page, "/html/body/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div")

    for div_c in range(div_count):
        div_texts = xpath_html_value(html_page,
                                     "/html/body/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[" + str(
                                         div_c + 1) + "]//text()")

        # /html/body/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/a
        href = xpath_html_value(html_page,
                                "/html/body/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[" + str(
                                    div_c + 1) + "]/a/@href")
        # http://data.taiesport.com/data/dota/leagueDetail?league_id=nt2681gmbcxtv7v5lepzu
        # /data/dota/leagueDetail?league_id=nt2681rme9xsvlvoh0vym
        id = str(href[0]).split("=")[1]
        div_list = []
        div_list.append(id)
        for div_text in div_texts:
            div_t = str(div_text).replace("\n", "").strip(" ")
            if int(len(div_t)) != 0:
                div_list.append(div_t)

        div_list.append("http://data.taiesport.com" + href[0])
        response_api("/ydj/save_saishizhongxin", div_list)


if __name__ == '__main__':
    taiesport_saishizhongxin()
