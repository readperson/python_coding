from tools.json_package.json_package import json_package
from tools.requests_api import requests_api
import json
import requests


# json={"gameId":"30564","version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"cb960de6bea9ce2825a63fcb97f251b02f01ef1e"}
def scoreboard(gameId, headers):
    # 积分 gameId
    url = "https://online.greenplayer.cn/E901D2019YBT/api/game/getGroupMatchRank.php"
    data = 'json={"gameId":"' + gameId + '","version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"cb960de6bea9ce2825a63fcb97f251b02f01ef1e"}'
    scoreboard = requests.post(url=url, headers=headers, data=data)
    scoreboard.encoding = "utf-8"
    scoreboard = str(scoreboard.text).replace("﻿", "")
    scoreboard = json.loads(scoreboard)

    scoreboard_count = int(len(scoreboard["returndata"]))
    print("scoreboard", scoreboard)
    word_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]
    returndata_list = []

    # scoreboard_list1 = []
    for s_count in range(scoreboard_count):

        # ss = scoreboard["returndata"][s_count]
        word = word_list[s_count]
        # print("word", word)
        if word in scoreboard["returndata"][s_count]:
            word_count = int(len(scoreboard["returndata"][s_count][word]))
            # print("  word_count", word_count)
            scoreboard_list = []
            # word_dict = {}
            for w_count in range(word_count):
                scoreboard_dict = {}
                json_package(scoreboard["returndata"][s_count][word][w_count], "teamId", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "teamName", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "portrait", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "place", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "success", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "dual", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "lose", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "credit", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "NetScore", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "Score", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "closedCredit", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "closedNetScore", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "closedScore", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "haveSmallCycle", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "eliminate", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "rank", "", scoreboard_dict)
                json_package(scoreboard["returndata"][s_count][word][w_count], "totalMatch", "", scoreboard_dict)
                returndata_list.append(scoreboard_dict)
            # word_dict[word] = scoreboard_list
            # returndata_list.append(scoreboard_list)

        # if "teamId" in scoreboard["returndata"][s_count]:
        #     scoreboard_dict1 = {}
        #     json_package(scoreboard["returndata"][s_count], "teamId", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "teamName", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "portrait", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "place", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "success", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "dual", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "lose", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "credit", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "NetScore", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "Score", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "closedCredit", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "closedNetScore", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "closedScore", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "haveSmallCycle", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "eliminate", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "rank", "", scoreboard_dict1)
        #     json_package(scoreboard["returndata"][s_count], "totalMatch", "", scoreboard_dict1)
        #     returndata_list.append(scoreboard_dict1)
        # else:
        #     returndata_list = []
    print("returndata", returndata_list)

    return returndata_list


if __name__ == '__main__':
    # 31957   无 33450 32214 a-h   33686
    gameId = "34562"
    headers = {'Host': 'online.greenplayer.cn', 'Connection': 'close', 'Accept': 'application/json,text/plain,*/*',
               'Origin': 'https',
               'User-Agent': 'Dalvik/2.1.0(Linux;U;Android5.1.1;HMA-AL00Build/LMY48Z)/GreenAppVersionCode=85/GreenAppVersionName=8.5.1_Android',
               'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'https',
               'Accept-Encoding': 'gzip,deflate', 'Accept-Language': 'zh-CN,en-US;q=0.8',
               'X-Requested-With': 'cn.greenplayer.zuqiuke'}

    scoreboard(gameId, headers)
