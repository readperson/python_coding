import requests
import json


def requests_api(url,headers, data):
    response = requests.post(url=url, headers=headers, data=data)
    response = json.loads(response.text)
    return response


