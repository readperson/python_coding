import sys

from tools.file_system_path import file_system_path

sys.path.append(file_system_path())
from tools.params.params_handle import params_handle
from tools.get_time import getNowTime
from tools.params.sign_handle import sign_handle
from tools.params.data_handle import data_handle
from api.requests_api import request_post
from tools.login_cache.login_cache import get_login_cahe
from tools.url_cahe.url_cahe import get_url


def params_requests_handle(method, params):
    '''
    对所有共性请求进行封装
    传入参数：params, method, url, ctx_id, salt
    :param params:
    :param method:
    :param ctx_id:
    :param salt:
    :return: request_post(data_handle(method, sign, params, timestamp, ctx_id), method)
    '''
    params_base64 = params_handle(params)
    method = method
    timestamp = getNowTime()
    url = get_url()
    sign = sign_handle(get_login_cahe().get("salt"), method, params_base64, get_login_cahe().get("ctx_id"), timestamp)
    return request_post(data_handle(method, sign, params_base64, timestamp, get_login_cahe().get("ctx_id")), method,
                        params, url)
