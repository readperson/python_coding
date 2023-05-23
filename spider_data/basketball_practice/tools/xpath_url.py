import requests
from lxml import etree
from urllib.request import urlretrieve
import random
from tools.time_treatment import now_time_revert


def xpath_network_url_handle(url):
    session_page = requests.session()
    response_page = session_page.get(url)
    html_str_page = response_page.content.decode("utf-8")
    html_page = etree.HTML(html_str_page)

    return html_page


def write_html(write_url, url_name):
    html_file = "../tools/html_file/"
    html_name = html_file + url_name + ".html"
    urlretrieve(write_url, html_name)
    return html_name


def write_html_page(html_name, count_record):
    html_page = red_html(html_name)
    pageCount = html_page.xpath('count(' + count_record + ')')
    if pageCount <= 3:
        return 0
    else:
        page = pageCount - 3
        return page


def xpath_count_record_number(html_name, count_record):
    html_page = red_html(html_name)
    record_number = int(html_page.xpath('count(' + count_record + ')'))
    return record_number


def get_local_html_text_attribute(html_name, textAttr):
    html_page = red_html(html_name)
    textAndAttr = html_page.xpath(textAttr)
    return textAndAttr


def red_html(html_name):
    with open(html_name, encoding="utf-8") as f:
        html_text = f.read()
        html_page = etree.HTML(html_text)
    return html_page


def get_network_html_text_attribute(html_page, textAttr):
    textAndAttr = html_page.xpath(textAttr)
    return textAndAttr


def get_network_html_count(html_page, count_record):
    record_number = html_page.xpath('count(' + count_record + ')')
    return record_number


def xpath_string_handle(string_s):
    return str(string_s).replace("['", "").replace("']", "")


def handle_first_dict(url_result_name, c_r_number):
    img_number = random.randint(1, 27)
    page_view = random.randint(1000, 3000)
    time_random = random.randint(40, 150)

    pracite_dict = {}
    href_a = "/html/body/div[1]/div/div/div[2]/li[" + str(c_r_number) + "]/div[1]/a[1]/@href"
    href_a = xpath_string_handle(get_local_html_text_attribute(url_result_name, href_a))
    # img = "/html/body/div[1]/div/div/div[2]/li[" + str(c_r_number) + "]/div[1]/a[1]/img/@src"
    # img = xpath_string_handle(get_local_html_text_attribute(url_result_name, img))
    img_text = "/html/body/div[1]/div/div/div[2]/li[" + str(c_r_number) + "]/div[1]/a[2]/text()"
    img_text = xpath_string_handle(get_local_html_text_attribute(url_result_name, img_text))
    title = "/html/body/div[1]/div/div/div[2]/li[" + str(c_r_number) + "]/div[2]/h3/a/text()"
    title = xpath_string_handle(get_local_html_text_attribute(url_result_name, title))
    summary = "/html/body/div[1]/div/div/div[2]/li[" + str(c_r_number) + "]/div[2]/p[1]/text()"
    summary = xpath_string_handle(get_local_html_text_attribute(url_result_name, summary))
    # author = "/html/body/div[1]/div/div/div[2]/li[" + str(c_r_number) + "]/div[2]/p[2]/span[1]/text()"
    # author = xpath_string_handle(get_local_html_text_attribute(url_result_name, author))
    # page_View = "/html/body/div[1]/div/div/div[2]/li[" + str(c_r_number) + "]/div[2]/p[2]/span[3]/text()"
    # page_view = xpath_string_handle(get_local_html_text_attribute(url_result_name, page_View))
    # publish_time = "/html/body/div[1]/div/div/div[2]/li[" + str(c_r_number) + "]/div[2]/p[2]/span[4]/text()"
    # publish_time = xpath_string_handle(get_local_html_text_attribute(url_result_name, publish_time))
    pracite_dict["id"] = href_a.split("/")
    id_count = int(len(pracite_dict["id"]))
    pracite_dict["type_text"] = img_text
    if id_count == 3:
        pracite_dict["id"] = href_a.split("/")[2].split(".")[0]
    else:
        pracite_dict["id"] = href_a.split("/")[4].split(".")[0]
    pracite_dict["href_a"] = href_a
    pracite_dict["img"] = "<img src ='http://47.97.79.60/content/basketball/xunlian/" + str(img_number) + ".jpg'>"
    pracite_dict["img_carousel"] = "http://47.97.79.60/content/basketball/xunlian/" + str(img_number) + ".jpg"
    pracite_dict["title"] = title
    pracite_dict["summary"] = "<p>" + summary + "</p>"
    pracite_dict["author"] = "篮球约"
    pracite_dict["page_view"] = page_view
    pracite_dict["publish_time"] = now_time_revert(time_random)
    return pracite_dict
