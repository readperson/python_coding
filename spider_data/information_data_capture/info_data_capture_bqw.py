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


# 中国冰球协会
def info_data_capture_dqw():
    time_minutes = 0
    for page in range(5):

        page = page + 1
        url = "http://icehockey.sport.org.cn/news/list_1384_" + (str(page)) + ".html"
        session = requests.session()
        response = session.get(url)
        html_str = response.content.decode("utf-8")
        html = etree.HTML(html_str)
        li_count = html.xpath("count(/html/body/div[3]/ul/li)")
        print(li_count)
        base = {}

        for i in range(int(li_count)):
            time_minutes = time_minutes + 19
            capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
            publishTime = (datetime.datetime.now() + datetime.timedelta(minutes=-time_minutes)).strftime(
                "%Y-%m-%d %H:%M:%S")
            i = i + 1
            a_href = html.xpath("/html/body/div[3]/ul/li[" + str(i) + "]/a/@href")
            a_href = str(a_href).replace("['", "").replace("']", "")
            # print(a_href)
            ids = a_href.split("/")
            id = ids[int(len(ids)) - 1].split(".")[0]
            # print(id)
            # http://icehockey.sport.org.cn/news/2020/0623/334044.html
            response_info = session.get(a_href)
            html_info_str = response_info.content.decode("utf-8")

            html_info = etree.HTML(html_info_str)
            # print("html_info:", html_info)

            # 'articleTitle': '尤文图斯2-0基辅迪纳摩，莫拉塔梅开二度',  # 资讯标题
            #    /html/body/div[3]/div[2]/h2
            articleTitle = html_info.xpath("/html/body/div[3]/div[2]/h2/text()")
            articleTitle = str(articleTitle).replace("['", "").replace("']", "")
            # 'articleId': '700889'  # 文章ID
            articleId = id
            # 'articleViewCount': '172',  # 阅读
            articleViewCount = str(random.randint(100, 2000))
            # 'articleGoodCount': '9',  # 点赞数
            articleGoodCount = str(random.randint(100, 2000))

            # 'articleArthurNickname': '比利时杨坤',  # 发布人昵称
            articleArthurNickname = "中国冰球协会"
            # 'HeadImgUrl': 'https://static.qiuhui.com/avatar/7db3c1b8-6047-45cc-8070-8d595ea868e2.jpg',
            HeadImgUrl = "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2812384179,604900572&fm=15&gp=0.jpg"
            # 'tagName': 'CBA',  # 标签
            tagName = "中国冰球"
            # /html/body/div[3]/div[2]/div/span[1]
            # publishTime = html_info.xpath("/html/body/div[3]/div[2]/div/span[1]/text()")
            # publishTime = str(publishTime).replace("['", "").replace("']", "")
            publishTime = publishTime
            publishTimeStr = "1小时前"
            content_count = html_info.xpath("count(/html/body/div[3]/div[2]/p)")
            articleContent = ""
            htmlContent = ""
            for c_count in range(int(content_count)):
                c_count = c_count + 1
                # /html/body/div[3]/div[2]/p[2]/img
                img_count = html_info.xpath("count(/html/body/div[3]/div[2]/p[" + str(c_count) + "]/img)")
                if img_count == 1:
                    imageStr = html_info.xpath("/html/body/div[3]/div[2]/p[" + str(c_count) + "]/img/@src")
                    imageStr = str(imageStr).replace("['", "").replace("']", "")
                    imageStrUrl = str(imageStr).replace("['", "").replace("']", "")
                    imageStr = "<p align='center'><img src=" + imageStr + "></img></p></br>"
                    htmlContent = htmlContent + imageStr

                else:
                    # /html/body/div[3]/div[2]/p[1]
                    content = html_info.xpath("/html/body/div[3]/div[2]/p[" + str(c_count) + "]/text()")
                    content_child = html_info.xpath("/html/body/div[3]/div[2]/p[" + str(c_count) + "]/*/text()")
                    content_child = str(content_child).replace("['", "").replace("']", "")
                    if content_child != "[]":
                        content = "<strong>" + content_child + "</strong>"

                    # print("content",str(content))
                    content = str(content).replace("['", "").replace("']", "")
                    content = "<p>" + content + "</p></br>"
                    articleContent = articleContent + content
                    htmlContent = htmlContent + content
            base["come_from"] = "中国冰球网"
            base["capture_time"] = capture_time
            base["capture_type"] = "冰球"

            base["articleTitle"] = articleTitle
            base["articleId"] = articleId
            base["articleViewCount"] = articleViewCount
            base["articleGoodCount"] = articleGoodCount
            base["articleArthurNickname"] = articleArthurNickname
            base["HeadImgUrl"] = HeadImgUrl
            base["tagName"] = tagName
            base["publishTime"] = publishTime
            base["publishTimeStr"] = publishTimeStr
            base["imageStr"] = imageStrUrl
            # articleContent = articleContent.replace("\\r\\n\\t", "</br>").replace("\\u3000\\u3000", "")
            articleContent = articleContent.replace("\\r", "").replace("\\n", "").replace("\\t", "").replace("\\u3000",
                                                                                                             "")
            articleContent = articleContent.replace("\r", "").replace("\n", "").replace("\t", "").replace("\u3000", "")
            articleContent = articleContent.replace("\xa0", "").replace("\\xa0", "")
            articleContent = articleContent

            htmlContent = htmlContent.replace("\\r", "").replace("\\n", "").replace("\\t", "").replace("\\u3000", "")
            htmlContent = htmlContent.replace("\r", "").replace("\n", "").replace("\t", "").replace("\u3000", "")
            htmlContent = htmlContent.replace("\xa0", "").replace("\\xa0", "")
            htmlContent = htmlContent
            base["articleContent"] = articleContent
            print("htmlContent:", htmlContent)
            base["htmlContent"] = text_conversion_base64(htmlContent)

            # print("组装成功的json数据", str(base).replace("'", '"'))
            # print("")
            # print(base)
            url_tj = "/news/save_news"
            response_api(url_tj, base)


if __name__ == '__main__':
    info_data_capture_dqw()
