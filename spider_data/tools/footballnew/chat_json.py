from tools.headers import headers_header
import json
import requests


# 聊天
def chat_json(matchId):
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    chat_url = "https://mobile-gate.611.com/api/ChatRoomMsg"
    chat_headers = {
        "source": source,
        "lytime": lytime,
        "deviceid": deviceid,
        "deviceaid": deviceaid,
        "requestRam": requestRam,
        "sign": sign
    }

    # 聊天
    chat_data = {"ChatRoomId": str(matchId) + "0"}
    chat_rep = requests.post(url=chat_url, data=chat_data, headers=chat_headers).text
    chat_rep = json.loads(chat_rep)
    chat_dicts = {}
    chat_dicts["matchId"] = matchId
    chat_list = []
    lt_count = int(len(chat_rep["data"]))
    if lt_count > 0:
        print("聊天记录数", lt_count)
    for chat_count in range(lt_count):
        chat_dict = {}
        chat_dict["id"] = chat_rep["data"][chat_count]["id"]
        chat_dict["chatRoomId"] = chat_rep["data"][chat_count]["chatRoomId"]
        chat_dict["nickName"] = chat_rep["data"][chat_count]["nickName"]
        chat_dict["chatMsg"] = str(chat_rep["data"][chat_count]["chatMsg"]).replace("盘口", "**").replace("赢",
                                                                                                        "*").replace(
            "输", "*")
        chat_dict["sendTime"] = chat_rep["data"][chat_count]["sendTime"]
        chat_dict["userId"] = chat_rep["data"][chat_count]["userId"]
        chat_list.append(chat_dict)
    chat_dicts["data"] = chat_list

    print("聊天", chat_dicts)


if __name__ == '__main__':
    chat_json(str(303494725))
