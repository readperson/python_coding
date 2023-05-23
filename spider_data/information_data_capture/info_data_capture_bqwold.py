import sys
sys.path.append("/opt/data_captureAPP")
import json
import requests
from lxml import etree
import random
from tools.get_to_ken import *
import datetime

# 中国冰球协会
def info_data_capture_dqw():
    time_minutes = 0
    for page in range(5):
        data = {"account": "17318203546", "password": "123456"}
        session = requests.session()
        post_obj = session.post("http://47.114.6.60/user/login", data)
        post_obj = post_obj.text
        post_obj = json.loads(post_obj)
        access = post_obj["data"]["val"]["access"]
        page = page + 1
        url = "http://icehockey.sport.org.cn/news/list_1384_" + (str(page)) + ".html"
        session = requests.session()
        response = session.get(url)
        html_str = response.content.decode("utf-8")
        html = etree.HTML(html_str)
        # /html/body/div[3]/ul/li[1]
        li_count = html.xpath("count(/html/body/div[3]/ul/li)")
        print(li_count)
        # /html/body/div[3]/ul/li[1]/a
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
            articleArthurNickname = "中国冰球"
            # 'HeadImgUrl': 'https://static.qiuhui.com/avatar/7db3c1b8-6047-45cc-8070-8d595ea868e2.jpg',
            HeadImgUrl = "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2812384179,604900572&fm=15&gp=0.jpg"
            # 'tagName': 'CBA',  # 标签
            tagName = ""
            # /html/body/div[3]/div[2]/div/span[1]
            # 'publishTime': '2020-10-21 02:48:58',  # 发布时间
            # publishTime = html_info.xpath("/html/body/div[3]/div[2]/div/span[1]/text()")
            # publishTime = str(publishTime).replace("['", "").replace("']", "")
            publishTime = publishTime
            # 'publishTimeStr': '6小时前',  # 后台算出
            publishTimeStr = "1小时前"
            # “come_from”: “趣运动”,
            # “capture_time”: '2020-11-09 10:00:37',
            content_count = html_info.xpath("count(/html/body/div[3]/div[2]/p)")
            print("content_count:--", content_count)
            articleContent = ""
            for c_count in range(int(content_count)):
                c_count = c_count + 1
                # /html/body/div[3]/div[2]/p[2]/img
                img_count = html_info.xpath("count(/html/body/div[3]/div[2]/p[" + str(c_count) + "]/img)")
                if img_count == 1:
                    imageStr = html_info.xpath("/html/body/div[3]/div[2]/p[" + str(c_count) + "]/img/@src")
                    imageStr = str(imageStr).replace("['", "").replace("']", "")

                else:
                    # /html/body/div[3]/div[2]/p[1]
                    Content = html_info.xpath("/html/body/div[3]/div[2]/p[" + str(c_count) + "]/text()")
                    Content = str(Content).replace("['", "").replace("']", "")
                    Content = "<p>" + Content + "</p></br>"
                    articleContent = articleContent + Content
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
            base["imageStr"] = imageStr
            articleContent = articleContent.replace("\\r\\n\\t", "</br>").replace("\\u3000\\u3000", "")
            base["articleContent"] = articleContent

            comm_url = "http://47.114.6.60/news/save_news"
            info_capture_json = json.dumps(base)
            print("组装成功的json数据", base)

            comm_headers = {"Content-Type": "application/json;charset=utf-8",
                            "Authorization": "Bearer " + access}
            print("请求url:", comm_url)
            print("请求头:", comm_headers)
            print("请求数据:", info_capture_json)
            result = requests.post(url=comm_url, data=info_capture_json, headers=comm_headers)
            print("请求返回状态码：", result.status_code)
            print(result.text)
            print("")
            # print(base)


if __name__ == '__main__':
    info_data_capture_dqw()
