import json
import requests


url_chat = "https://app-gateway.leisu.com/v1/app/chat/history?room_id=R4_1_3532890&auth_key=1605233990-0-0-9eb939279f58da924658db1f8e0e12ec"
header_chat = {
    "sn": "003dca5d",
    "device_id": "1507bfd3f77dfd86703",
    "aid": "c20964cf79411c67",
    "time": "1605090558",
    "sign": "8d84ade2abc47cf4f2a7411920326af2",
    "cdid": "c387b94e-765f-30c7-857e-c1ca7fe0144a",
    "start": "1604299428"
}
result_chat = requests.get(url=url_chat, headers=header_chat)
print(result_chat.text)