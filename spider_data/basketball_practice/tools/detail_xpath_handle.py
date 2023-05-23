from basketball_practice.tools.xpath_url import red_html
from lxml import etree
import re
from tools.base64_text import text_conversion_base64


def first_div(html_file_name):
    return red_html(html_file_name)


def first_div_list_text(file_name, practie_detail_list):
    html_page = first_div(file_name)
    # /html/body/div[1]/div/div/div[1]/div[1] /html/body/div[1]/div/div/div[2]/div[1]
    # /html/body/div[1]/div/div/div[2]/div[1]
    #     #
    f_text = html_page.xpath(".//div[@class='detail_article']/text()")
    text_first = first_text(f_text).split("帮助。")
    practie_detail_list.insert(0, "<p>" + text_first[0] + "帮助。</p>")
    practie_detail_list.insert(len(practie_detail_list), "</p>" + text_first[1] + "</p>")
    return practie_detail_list


def first_text(s_text):
    return str(s_text).replace("'\\n',", "").replace("\\xa0", "").replace("['", "").replace("']", "").replace("'\\n",
                                                                                                              "").replace(
        "\\n", "").replace("',", "").replace(" ", "")


def str_text(string_s):
    text = str(string_s).replace("[", "").replace("]", "").replace("\\n", "").replace("\\t", "").replace("\\xa0",
                                                                                                         "").replace(
        '"', "").replace("'", "").replace(",", "").replace(" ", "")
    return text


# 文件 div
def detail_xpath_dandle(html_path, countNmber, practie_detail_list):
    html_page = red_html(html_path)
    # 的判断该元素下是否有子元素 有返回1 没有返回0
    #  /html/body/div[2]/div/div/div[1]/div[1]/div[1]/p/font/a
    # /html/body/div[1]/div/div/div[1]/div[1]/div[1]
    # /html/body/div[1]/div/div/div[2]/div[1]/div
    # ".//div[@class='detail_article']/div"
    a = html_page.xpath("count(.//div[@class='detail_article']/div[" + str(countNmber) + "]/p/a)")
    if a == 1:
        img = str_text(html_page.xpath(
            ".//div[@class='detail_article']/div[" + str(countNmber) + "]/p/a/@href"))
        #
        # practie_detail_list.append("http://www.lanqiuhuo.com" + img)
        practie_detail_list.append("<img src ='http://www.lanqiuhuo.com" + img + "'>")


    else:
        # /html/body/div[1]/div/div/div[1]/div[1]/div[29]
        # /html/body/div[1]/div/div/div[2]/div[1]/div
        # /html/body/div[1]/div/div/div[1]/div[1]/div[1]
        # /html/body/div[1]/div/div/div[1]/div[1]/div[3]
        f_text = html_page.xpath(".//div[@class='detail_article']/div[" + str(countNmber) + "]//text()")
        # print("--", f_text)

        f_text = str(f_text).replace(" ", "").replace("'\\n\\t',", "").replace("'\\n\\t\\t',", "").replace(", '\\n'",
                                                                                                           "").replace(
            " ",
            "").replace(
            "['", "").replace("']", "").replace("'", "").replace("\\n\\t\\xa0", "").replace("\\n\\t", "").replace(
            "\\t\\xa0", "").replace("\\n", "").replace("\\t", "").replace("\\", "").replace("xa0", "")
        text_s = f_text.split(",")
        text_str = str(text_s).replace("['", "").replace("']", "")
        if int(len(text_str)) > 0:
            text_list = []
            for s_i in text_s:
                i_count = int(len(s_i))
                if i_count != 0:
                    text_list.append("<span>" + s_i + "</span>")
            practie_detail_list.append(text_list)
    return practie_detail_list


def detail_xpath_dandle1(html_path, countNmber, practie_detail_list):
    html_page = red_html(html_path)
    # 的判断该元素下是否有子元素 有返回1 没有返回0

    a = html_page.xpath("count(/html/body/div[1]/div/div/div[2]/div[1]/div[" + str(countNmber) + "]/p/a)")
    if a == 1:
        img = str_text(html_page.xpath(
            "/html/body/div[1]/div/div/div[2]/div[1]/div[" + str(countNmber) + "]/p/a/@href"))
        #
        # practie_detail_list.append("http://www.lanqiuhuo.com" + img)
        practie_detail_list.append("<img src ='http://www.lanqiuhuo.com" + img + "'>")

    else:

        f_text = html_page.xpath("/html/body/div[1]/div/div/div[2]/div[1]/div[" + str(countNmber) + "]//text()")
        # print("--", f_text)

        f_text = str(f_text).replace(" ", "").replace("'\\n\\t',", "").replace("'\\n\\t\\t',", "").replace(", '\\n'",
                                                                                                           "").replace(
            " ",
            "").replace(
            "['", "").replace("']", "").replace("'", "").replace("\\n\\t\\xa0", "").replace("\\n\\t", "").replace(
            "\\t\\xa0", "").replace("\\n", "").replace("\\t", "").replace("\\", "").replace("xa0", "")
        text_s = f_text.split(",")
        text_str = str(text_s).replace("['", "").replace("']", "")
        if int(len(text_str)) > 0:
            text_list = []
            for s_i in text_s:
                i_count = int(len(s_i))
                if i_count != 0:
                    text_list.append("<span>" + s_i + "</span>")
            practie_detail_list.append(text_list)
    return practie_detail_list


def html_content(file_name):
    html_page = red_html(file_name)
    f_text = html_page.xpath("//div[@class='detail_article']")
    str_div = ""
    for value in f_text:
        result = etree.tostring(value, encoding='utf-8')
        result = result.decode('utf-8')
        result = str(result).replace('<img src="', '<img src="http://www.lanqiuhuo.com')
        result = str(result)
        result = re.sub('href=".*?"', "href=''", result)
        result = re.sub('max-width.*?;"', "max-width: 100%;", result)
        result = re.sub('width.*?;"', "", result)
        result = re.sub('text-align: center;', "", result)
        str_div += result
    # print(str_div)
    return text_conversion_base64(str_div)


if __name__ == '__main__':
    # file_name = "../tools/html_file/24104.html"
    # html_page = first_div(file_name)
    # f_text = html_page.xpath("//div[@class='detail_article']")
    # str_div = ""
    # for value in f_text:
    #     result = etree.tostring(value, encoding='utf-8')
    #     result = result.decode('utf-8')
    #     # str_first = re.sub('<.*?>',"",str)
    #     result = str(result).replace('<img src="', '<img src="http://www.lanqiuhuo.com')
    #     result = str(result)
    #     result = re.sub('href=".*?"', "href=''", result)
    #     result = re.sub('max-width.*?;"', "max-width: 100%;", result)
    #     result = re.sub('width.*?;"', "", result)
    #     result = re.sub('text-align: center;', "", result)
    #     str_div += result
    # print(str_div)

    count = 50
    file_name = "../tools/html_file/24210.html"
    practie_detail_list = []
    html_page = first_div(file_name)
    # 多页 ../tools/html_file/24083.html
    # 多页 13.0
    # 多页 ../tools/html_file/24081.html
    # 多页 15.0
    # 多页 ../tools/html_file/24082.html
    # 多页 15.0
    f_text = html_page.xpath("//div[@class='detail_article']//text()")
    print(f_text)
    # text_first = first_text(f_text).split("帮助。")
    # for i in range(count):
    #     i += 1
    #     practie_detail_list = detail_xpath_dandle(file_name, i, practie_detail_list)
    # practie_detail_list.insert(0, text_first[0] + "帮助。")
    # practie_detail_list.insert(len(practie_detail_list), text_first[1])
    # print(practie_detail_list)
