import requests
import json
from tools.headers import headers_header
from tools.response_api import response_api


# 赛况  MatchID=303582849&SportType=1&ModeType=9&minTime=
def event_json(matchId):
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    events_url = "https://mobile-gate.611.com/api/LiveDetail"
    events_data = {"MatchID": str(matchId), "SportType": "1", "ModeType": "9", "minTime": ""}
    events_headers = {
        "source": source,
        "lytime": lytime,
        "deviceid": deviceid,
        "deviceaid": deviceaid,
        "requestRam": requestRam,
        "sign": sign
    }
    events_rep = requests.post(url=events_url, data=events_data, headers=events_headers).text
    events_rep = json.loads(events_rep)
    events = {}
    events["matchId"] = matchId
    events["events"] = events_rep["data"]
    response_api("/leyulanqiu/save_saikuang", events)
