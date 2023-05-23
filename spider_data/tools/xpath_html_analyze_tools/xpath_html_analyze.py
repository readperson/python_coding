from lxml import etree
import requests
import time


def request_post(url, data, headers):
    content = requests.post(url=url, data=data, headers=headers)
    html_str_page = content.content
    html_page = etree.HTML(html_str_page)
    print(html_page)
    return html_page


def request_get(url):
    content = requests.get(url=url)
    # print(content.content.decode("utf-8"))
    html_str_page = content.content
    html_page = etree.HTML(html_str_page)
    # print(html_page)
    return html_page


def xpath_html_page(url_page):
    session_page = requests.session()
    response_page = session_page.get(url_page)
    html_str_page = response_page.content
    html_page = etree.HTML(html_str_page)
    return html_page


def xpath_html_page_headers(url_page, headers):
    response_page = requests.get(url=url_page, headers=headers)
    html_str_page = response_page.content.decode("utf-8")
    # print(html_str_page)
    html_page = etree.HTML(html_str_page)
    return html_page


def xpath_html_count(html_page, xpath_count):
    xpath_count = int(html_page.xpath("count(" + xpath_count + ")"))
    return xpath_count


def xpath_html_value(html_page, xpath_text):
    xpath_text = html_page.xpath(xpath_text)
    return xpath_text


def write_html_backward_climb(write_url, url_name):
    html_file = "./html_file/"
    html_name = html_file + url_name + ".html"
    # print(url_name)
    headers = {
        "Host": "www.zyypp.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Cookie": "Hm_lvt_ce814af1f9888cca37acee8034c406d1=1611111524,1611134039,1611191752; PHPSESSID=nbq2la1gklo1obim0pdml673f6; Hm_lpvt_ce814af1f9888cca37acee8034c406d1=" + str(
            int(time.time())) + "; _wtspurl=/case/" + str(
            url_name) + ".html; _wtsuid=1c0a3eeb-94b7-431f-8079-9af7031c9da2; _wtscpk=3e28528e5e; _wtsexp=1611193073; _wtsjsk=252e5eb8e27fde2ac9cb9b48b0ff66d9",
        "Upgrade-Insecure-Requests": "1"}
    content = requests.get(url=write_url, headers=headers)
    content = content.content.decode("utf-8")
    with open(html_name, 'w', encoding="utf-8") as f:
        f.write(content)
    return html_name


def write_html(write_url, url_name):
    html_file = "./html_file/"
    html_name = html_file + url_name + ".html"
    # print(html_name)
    headers = {
        "Host": "www.zyypp.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Cookie": "_wtspurl=/case/jltd7e3/; _wtsuid=1c3b17b7-494c-4ca3-911a-b9887d11e046; _wtscpk=8110bd6be7; _wtsexp=1611120548; _wtsjsk=d1f550eb80f00a78696507c8a3b6ef8e; PHPSESSID=9c2nns88050ct0af33ia82ljs6;",
        "Upgrade-Insecure-Requests": "1"}
    content = requests.get(url=write_url, headers=headers)
    content = content.content.decode("utf-8")
    with open(html_name, 'w', encoding="utf-8") as f:
        f.write(content)
    return html_name


def red_html(html_name):
    with open(html_name, encoding="utf-8") as f:
        html_text = f.read()
        html_page = etree.HTML(html_text)
    return html_page
