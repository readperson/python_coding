import requests
import json
import time


def ticai():
    list_s = [
        ['04', '05', '06', '34', '35', '01', '12'],
        ['01', '03', '15', '31', '32', '02', '09'],
        ['07', '08', '21', '23', '34', '05', '06'],
        ['02', '19', '27', '32', '35', '07', '11'],
        ['13', '17', '21', '22', '23', '03', '08']]
    date = int(time.time())
    url = "https://api.xinti.com/chart/QueryPrizeDetailInfo"
    headers = {"Host": "api.xinti.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
               "Accept": "*/*",
               "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
               "Accept-Encoding": "gzip, deflate",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Origin": "https://www.xinti.com",
               "Connection": "close",
               "Referer": "https://www.xinti.com/prizedetail/dlt.html"}
    data = '{"ClientSource":3,"Param":{"GameCode":"DLT","IssuseNumber":""},"Date":' + str(
        date) + '835,"Token":"","Sign":"0a49015298468993bd69889883c4a9d0"}'

    rep = requests.post(url=url, headers=headers, data=data)
    rep = json.loads(rep.text)
    # print(rep)

    result = str(rep["Value"]["BonusPoolList"][0]["WinNumber"]).split("|")
    sum_s = str(result).replace("'", "").replace("[", "").replace("]", "").split(",")
    print(sum_s)
    # print(list_s)
    # for i in range(int(len(list_s))):
    #     print(list_s[i])
    #     prozone = 0
    #     postzone = 0
    #     for j in range(int(len(list_s[i]))):
    #         print(sum_s[j])
    #         if j <= 4:
    #
    #             if list_s[i][j] == sum_s[j]:
    #                 # print("--------")
    #                 # print(list_s[i][j])
    #                 prozone += 1
    #             print("prozone:", prozone)
    #
    #
    #         else:
    #             # print(list_s[i][j])
    #             if list_s[i][j] == sum_s[j]:
    #                 # print("=========")
    #                 # print(list_s[i][j])
    #                 postzone += 1
    #             print("postzone:", postzone)


# prozone = str(result[0]).split(",")
# postzone = str(result[1]).split(",")
# print(prozone)
# print(postzone)


if __name__ == '__main__':
    ticai()
