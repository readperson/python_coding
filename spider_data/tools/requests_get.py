import requests
import json


def requests_get(url):
    result = requests.get(url)
    result = json.loads(result.text)
    return result
