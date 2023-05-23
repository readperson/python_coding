import json
import requests
from lxml import etree


def model_analysis():
    url = "https://www.88lot.com/sports_web_h5/hd/allPrediction.html?token=2011241941269473915&secret=JLl859w4&userId=2011241941269383914&channelId=2005141447413819001&pageType=4&bcw=760"
    session = requests.session()
    response = session.get(url)
    html_str = response.content.decode("utf-8")
    html = etree.HTML(html_str)
    # /html/body/div/div[1]/div/h1
    AI_title = html.xpath("/html/body/div[1]/div[2]/div[2]/div/ul/li[1]/div/div[1]/div/div[1]/p/text()")
    print(AI_title)
    print("")


if __name__ == '__main__':
    model_analysis()
    if 1 == 1:
        print("11111111")
    elif 1 == 3:
        print("111111111")
