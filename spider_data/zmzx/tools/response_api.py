import sys

sys.path.append("/opt/data_captureAPP")
import requests

import json


def response_api(url, headers, data):
    data = json.dumps(data)
    result = requests.post(url=url, headers=headers, data=data)
    result = json.loads(result.text)
    return result
