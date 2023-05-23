import requests
import json


def get_to_ken():
    data = {"account": "17318203546", "password": "123456"}
    session = requests.session()
    post_obj = session.post("http://47.114.6.60/user/login", data)
    post_obj = post_obj.text
    post_obj = json.loads(post_obj)
    return post_obj["data"]["val"]["access"]
