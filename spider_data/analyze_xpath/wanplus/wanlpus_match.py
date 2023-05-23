from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.response_api import response_api


def wanlpus_match():
    url = "https://www.wanplus.com/lol/schedule"
    # /html/body/div[1]/div[2]/div[2]/div[3]/ul[1]/li[2]
    html_page = xpath_html_page(url)
    li_count = xpath_html_count(html_page, "/html/body/div[1]/div[2]/div[2]/div[3]/ul[1]/li")
    print(li_count)
    for li_c in range(li_count):
        div_text = xpath_html_value(html_page, "/html/body/div[1]/div[2]/div[2]/div[3]/ul[1]/li[" + str(
            li_c + 1) + "]/div//text()")
        img = xpath_html_value(html_page, "/html/body/div[1]/div[2]/div[2]/div[3]/ul[1]/li[" + str(
            li_c + 1) + "]/div[2]/a//@src")
        # print(div_text)
        href = xpath_html_value(html_page, "/html/body/div[1]/div[2]/div[2]/div[3]/ul[1]/li[" + str(
            li_c + 1) + "]/div[2]/a//@href")

        div_list = []

        for hr in href:
            id = str(hr).split("/")[3]
            div_list.append(id)

        for ig in img:
            div_list.append(ig)
        for d_text in div_text:
            div = str(d_text).replace("\r\n", "").strip(" ")
            if int(len(div)) != 0 and div != "查看详情":
                div_list.append(div)

        for hr in href:
            url = "https://www.wanplus.com" + str(hr)
            div_list.append(url)
            # https://www.wanplus.com/lol/team/4401
        response_api("/wjdj/save_kanbisai", div_list)
        print(div_list)


if __name__ == '__main__':
    wanlpus_match()
