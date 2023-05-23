import json
import requests
from lxml import etree


def model_analysis():
    url = "http://t.fkhongdan.com/module/spinach/enter.html?hdapp=hd&username=19865439671@fengkuangTY&userName=19865439671@fengkuangTY&userid=17062896&userId=17062896&newversion=android_10.6"
    session = requests.session()
    response = session.get(url)
    html_str = response.content.decode("utf-8")
    html = etree.HTML(html_str)
    # /html/body/div/div[2]/div/div[1]
    div_count = int(html.xpath('count(/html/body/div/div[2]/div/div)'))
    # /html/body/div/div[1]/div/h1
    AI_title = html.xpath("/html/body/div/div[1]/div/h1/text()")
    AI_content = html.xpath("/html/body/div/div[1]/div/p/text()")
    print(AI_title, AI_content)
    url_list = ["https://www.88lot.com/sports_web_mobile_transfer/jihai/authLogin?chanelId=2005141447413819001&userSign"
                "=49e0a6134326ea1c&timestamp=20201127192842&authCode=e1698446152fe5d48b1e8773743d10dc&modelType=bigDataReport",
                "https://www.88lot.com/sports_web_mobile_transfer/jihai/authLogin?chanelId=2005141447413819001&userSign"
                "=49e0a6134326ea1c&timestamp=20201127192842&authCode=e1698446152fe5d48b1e8773743d10dc&modelType=allAnalysis",
                "https://www.88lot.com/sports_web_mobile_transfer/jihai/authLogin?chanelId=2005141447413819001&userSign"
                "=49e0a6134326ea1c&timestamp=20201127192842&authCode=e1698446152fe5d48b1e8773743d10dc&modelType=coldJudge",
                "https://www.88lot.com/sports_web_mobile_transfer/jihai/authLogin?chanelId=2005141447413819001&userSign"
                "=49e0a6134326ea1c&timestamp=20201127192842&authCode=e1698446152fe5d48b1e8773743d10dc&modelType=oddsWave"]

    print(div_count)
    for d_count in range(div_count):
        # /html/body/div/div[2]/div/div[1]/div[1]/h2
        title1 = html.xpath("/html/body/div/div[2]/div/div[" + str(d_count + 1) + "]/div[1]/h2/text()")
        # /html/body/div/div[2]/div/div[1]/div[1]/h2/span
        title2 = html.xpath("/html/body/div/div[2]/div/div[" + str(d_count + 1) + "]/div[1]/h2/span/text()")
        print(title1, title2)
        # /html/body/div/div[2]/div/div[1]/div[2]/img
        image = html.xpath("/html/body/div/div[2]/div/div[" + str(d_count + 1) + "]/div[2]/img/@src")
        print(image)
        #  /html/body/div/div[2]/div/div[1]/div[2]/div/p
        content = html.xpath("/html/body/div/div[2]/div/div[" + str(d_count + 1) + "]/div[2]/div/p/text()")
        print(content)
        # /html/body/div/div[2]/div/div[1]/div[2]/div/div/span
        price = html.xpath("/html/body/div/div[2]/div/div[" + str(d_count + 1) + "]/div[2]/div/div/span/text()")
        print(price)

        # /html/body/div/div[2]/div/div[1]
        url_coneten = url_list[d_count]
        headers_coneten = {"Host": "www.88lot.com",
                           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
                           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                           "Accept-Encoding": "gzip, deflate",
                           "Connection": "close",
                           "Referer": "http://t.fkhongdan.com/module/spinach/enter.html?hdapp=hd&username=19865439671@fengkuangTY&userName=19865439671@fengkuangTY&userid=17062896&userId=17062896&newversion=android_10.6",
                           "Cookie": "JSESSIONID=76E9CCB0FB5204EFF49F6E181A443A72;secret=JLl859w4;userId=2011241941269383914;token=2011241941269473915",
                           "Upgrade-Insecure-Requests": "1"}
        # rep = requests.get(url=url_coneten, headers=headers_coneten,allow_redirects=False,verify=False).headers["Location"]
        rep = requests.get(url=url_coneten, headers=headers_coneten).history

        # print(rep[0].headers)
        # print(f'获取重定向的历史记录：{rep}')
        # print(f'获取第一次重定向的headers头部信息：{rep[0].headers}')
        print(type(rep))
        print(len(rep))
        print(rep[0].headers["Location"])




        print("")


if __name__ == '__main__':
    model_analysis()
