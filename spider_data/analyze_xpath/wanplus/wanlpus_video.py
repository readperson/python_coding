from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_count
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_value
from tools.xpath_html_analyze_tools.xpath_html_analyze import xpath_html_page
from tools.response_api import response_api


def wanlpus_video():
    url = "http://www.wanplus.com/dota2/video"
    html_page = xpath_html_page(url)
    li_count = xpath_html_count(html_page, "/html/body/div[1]/div[3]/div[3]/div[3]/ul/li")
    # http://www.wanplus.com/dota2/video/1189708
    video = {}
    for li_c in range(li_count):
        href = xpath_html_value(html_page,
                                "/html/body/div[1]/div[3]/div[3]/div[3]/ul/li[" + str(li_c + 1) + "]/a/@href")
        imgage = xpath_html_value(html_page,
                                  "/html/body/div[1]/div[3]/div[3]/div[3]/ul/li[" + str(li_c + 1) + "]/a/img/@src")
        title = xpath_html_value(html_page,
                                 "/html/body/div[1]/div[3]/div[3]/div[3]/ul/li[" + str(li_c + 1) + "]/a/img/@alt")
        video["title"] = str(title[0]).replace("\u200b", "").strip(" ")
        video["pkey"] = str(href[0]).split("/")[3]
        video["video_url"] = "http://www.wanplus.com" + str(href[0])
        video["imgage"] = imgage[0]
        response_api("/wjdj/save_shipin", video)

        # print(video)


if __name__ == '__main__':
    wanlpus_video()
