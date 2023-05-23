from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page


def wanmei_paihanbang():
    url = "https://pvp.wanmei.com/csgo/ranking.ladder"
    html_page = xpath_html_page(url)
    tr_count = xpath_html_count(html_page, "/html/body/div/div[3]/div/div/div[2]/div/table[2]//tr/td")
    # tr_count = xpath_html_count(html_page, "//*[@class='max-20']/tr")
    print(tr_count)


if __name__ == '__main__':
    wanmei_paihanbang()
