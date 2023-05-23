import sys
sys.path.append("/opt/data_captureAPP")
import json
import requests
from lxml import etree
import random
from tools.get_to_ken import *
import datetime

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
        data = {"account": "17318203546", "password": "123456"}
        session = requests.session()
        post_obj = session.post("http://47.114.6.60/user/login", data)
        post_obj = post_obj.text
        post_obj = json.loads(post_obj)
        access = post_obj["data"]["val"]["access"]
        time_minutes = time_minutes + 13
        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime(
            "%Y-%m-%d %H:%M:%S")
        now_time = (datetime.datetime.now() + datetime.timedelta(minutes=-time_minutes)).strftime(
            "%Y-%m-%d %H:%M:%S")
        i = i + 1
        #     'articleTitle': '尤文图斯2-0基辅迪纳摩，莫拉塔梅开二度', #资讯标题
        #     'articleId': '700889' #文章ID
        # 	'articleViewCount': '172', #阅读
        # 	'articleGoodCount': '9', #点赞数
        # 	'articleArthurNickname': '比利时杨坤', #发布人昵称
        # 'HeadImgUrl':'https://static.qiuhui.com/avatar/7db3c1b8-6047-45cc-8070-8d595ea868e2.jpg',头像
        # 	'tagName': 'CBA', #标签
        # 	'publishTime': '2020-10-21 02:48:58', #发布时间
        # 	'publishTimeStr': '6小时前',#后台算出
        # “come_from”: “趣运动”,
        # 	“capture_time”: '2020-11-09 10:00:37',
        # 	'imageStr':'https://static.qiuhui.com/avatar/c0ab73882ef1ee64a2.jpg',
        # 	'articleContent':

        #     /html/body/div[2]/div[2]/div/div/ul/li[1]/a
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
        for c_count in range(int(content_count)):
            c_count = c_count + 1
            # /html/body/div[2]/div[1]/div[1]/div[2]/p[10]
            imageStr = html_info.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/img/@src")
            imageStr = str(imageStr).replace("['", "").replace("']", "")
            img_count = html_info.xpath("count(/html/body/div[2]/div[1]/div[1]/div[2]/p[" + str(c_count) + "]/img)")
            if img_count == 1:
                imageStr = html_info.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/p[" + str(c_count) + "]/img/@src")
                imageStr = str(imageStr).replace("['", "").replace("']", "")


            else:
                # /html/body/div[3]/div[2]/p[1]
                Content = html_info.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/p[" + str(c_count) + "]/text()")
                Content = str(Content).replace("['", "").replace("']", "")
                Content = "<p>" + Content + "</p><br>"
                articleContent = articleContent + Content

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
        articleContent = articleContent.replace("\\r\\n\\t", "</br>").replace("\\u3000\\u3000", "").replace("<p>[]</p>", "")
        base["articleContent"] = "<span>" + articleContent+"</span>"
        print(base)
        comm_url = "http://47.114.6.60/news/save_news"
        info_capture_json = json.dumps(base)

        comm_headers = {"Content-Type": "application/json;charset=utf-8",
                        "Authorization": "Bearer " + access}
        print("请求url:", comm_url)
        print("请求头:", comm_headers)
        print("请求数据:", info_capture_json)
        result = requests.post(url=comm_url, data=info_capture_json, headers=comm_headers)
        print("请求返回状态码：", result.status_code)
        print(result.text)
        print("")

        # print("count_content", count_content)

    # print(li_count)


if __name__ == '__main__':
    inf_data_capute_glq()
