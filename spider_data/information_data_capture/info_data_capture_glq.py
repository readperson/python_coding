import sys

sys.path.append("/opt/data_captureAPP")
import json
import requests
from lxml import etree
import random
from tools.get_to_ken import *
import datetime
from tools.base64_text import text_conversion_base64
from tools.response_api import response_api


# 橄榄球
def inf_data_capute_glq():
    url = "http://www.nflchina.com/news/list/page-1"
    session = requests.session()
    response = session.get(url)
    html_str = response.content.decode("utf-8")
    #
    html = etree.HTML(html_str)
    # /html/body/div[2]/div[2]/div/div/ul/li[1]

    li_count = html.xpath("count(/html/body/div[2]/div[2]/div/div/ul/li)")
    base = {}
    time_minutes = 0
    for i in range(int(li_count)):
        time_minutes = time_minutes + 13
        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime(
            "%Y-%m-%d %H:%M:%S")
        now_time = (datetime.datetime.now() + datetime.timedelta(minutes=-time_minutes)).strftime(
            "%Y-%m-%d %H:%M:%S")
        i = i + 1
        base["come_from"] = "NFL在中国"
        base["capture_time"] = capture_time
        base["capture_type"] = "橄榄球"
        articleTitle = html.xpath("/html/body/div[2]/div[2]/div/div/ul/li[" + str(i) + "]/a/@title")
        articleTitle = str(articleTitle).replace("['", "").replace("']", "")
        articleViewCount = str(random.randint(100, 2000))
        articleGoodCount = str(random.randint(100, 2000))
        articleArthurNickname = "NFL在中国"
        HeadImgUrl = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1604916632270&di=6a1c25c0c570923085776ac41960fbe4&imgtype=0&src=http%3A%2F%2Fbpic.588ku.com%2Felement_origin_min_pic%2F16%2F09%2F15%2F2357dac1a2c8264.jpg"
        tagName = 'NFL'
        publishTime = now_time

        a_href = html.xpath("/html/body/div[2]/div[2]/div/div/ul/li[" + str(i) + "]/a/@href")
        a_href = str(a_href).replace("['", "").replace("']", "")
        ids = a_href.split("/")
        id = ids[int(len(ids)) - 1].split(".")[0]
        articleId = id

        response_info = session.get(a_href)
        html_info_str = response_info.content.decode("utf-8")

        html_info = etree.HTML(html_info_str)

        # /html/body/div[2]/div[2]/div/div/ul/li[1]/a/div[1]/img/@src
        # /html/body/div[2]/div[1]/div[1]/div[2]/p
        content_count = html_info.xpath("count(/html/body/div[2]/div[1]/div[1]/div[2]/p)")
        print("count_content", content_count)
        articleContent = ""
        htmlContent = ""
        for c_count in range(int(content_count)):
            c_count = c_count + 1
            # /html/body/div[2]/div[1]/div[1]/div[2]/p[10]
            imageStr = html_info.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/img/@src")
            imageStr = str(imageStr).replace("['", "").replace("']", "")
            img_count = html_info.xpath("count(/html/body/div[2]/div[1]/div[1]/div[2]/p[" + str(c_count) + "]/img)")
            if img_count == 1:
                imageStr = html_info.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/p[" + str(c_count) + "]/img/@src")
                imageStr = str(imageStr).replace("['", "").replace("']", "")
                imageStr = "<p><img src=" + imageStr + "></p></br>"
                htmlContent = htmlContent + imageStr


            else:
                # /html/body/div[3]/div[2]/p[1]
                content = html_info.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/p[" + str(c_count) + "]/text()")
                content_child = html_info.xpath(
                    "/html/body/div[2]/div[1]/div[1]/div[2]/p[" + str(c_count) + "]/*/text()")
                content_child = str(content_child).replace("[", "").replace("]", "").replace("'", "").replace(",", "")
                if content_child != "":
                    print("content_child--==", content_child)
                    content = "<strong>" + content_child + "</strong>"
                content = str(content).replace("['", "").replace("']", "")
                content = "<p>" + content + "</p></br>"
                articleContent = articleContent + content
                htmlContent = htmlContent + content

        base["articleTitle"] = articleTitle
        base["articleId"] = articleId
        base["articleViewCount"] = articleViewCount
        base["articleGoodCount"] = articleGoodCount
        base["articleArthurNickname"] = articleArthurNickname
        base["HeadImgUrl"] = HeadImgUrl
        base["tagName"] = tagName
        base["publishTime"] = publishTime
        base["publishTimeStr"] = "1小时前"
        base["imageStr"] = imageStr
        articleContent = articleContent.replace("\\r\\n\\t", "").replace("\\u3000\\u3000", "").replace("[]", "")
        htmlContent = htmlContent.replace("\\r\\n\\t", "").replace("\\u3000\\u3000", "").replace("[]", "")
        base["articleContent"] = articleContent
        base["htmlContent"] = text_conversion_base64(htmlContent)
        url_tj = "/news/save_news"
        response_api(url_tj, base)


if __name__ == '__main__':
    inf_data_capute_glq()
