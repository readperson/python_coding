from tools.url_cahe.url_cahe import get_url
from api.requests_api import request_get_json
from api.requests_api import reques_post_form
from api.requests_api import request_session_get
from api.requests_api import request_session_post
from tools.json_header.json_header import json_header
from tools.json_header.json_header import from_post_header
from tools.json_header.json_header import sesssion_header


def request_tempplet_json_get(url_params):
    url = get_url() + url_params
    header = json_header()
    return request_get_json(url, header)


def request_tempplet_form_post(url_, data):
    url = get_url() + url_
    header = from_post_header()
    return reques_post_form(url, data, header)


def request_tempplet_seession_get(url_):
    url = get_url() + url_
    header = sesssion_header()
    return request_session_get(url, header)


def request_tempplet_seession_post(url_, data):
    url = get_url() + url_
    header = sesssion_header()
    return request_session_post(url, data, header)
