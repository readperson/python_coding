import requests
import json
from tools.headers import headers_header
from tools.response_api import response_api


# 赛况  MatchID=303580977&SportType=1&ModeType=9&minTime=
def event_json(matchId):
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    events_url = "https://mobile-gate.611.com/api/LiveDetail"
    events_data = {"MatchID": str(matchId), "SportType": "0", "ModeType": "9", "minTime": ""}
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
    # data
    events = {}
    events["matchId"] = matchId
    events_str = str(events_rep["data"]).replace("False", "''").replace("'", '"')
    events["events"] = json.loads(events_str)
    response_api("/leyuzuqiu/save_saikuang", events)


if __name__ == '__main__':
    event_json("303490720")
