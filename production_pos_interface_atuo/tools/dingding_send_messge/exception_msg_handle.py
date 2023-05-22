import sys
from tools.file_system_path import file_system_path

sys.path.append(file_system_path())
from tools.get_time import get_now_time


# url, method, header, data, result
def exception_msg_handle(url, params, method, header, data, result):
    '''
    :param url:
    :param header:
    :param data:
    :param result:
    :return:
    '''
    msg = "后端中台SCRM接口错误\r\n 【时间】:  " + str(get_now_time()) + "\r\n 【URL】:  " + str(url) + "\r\n 【PARAMS】： " + str(
        params) + "\r\n【METHOD】:  " + str(method) + "\r\n 【HEADER】:  " + str(header) + "\r\n 【DATA】:  " + str(
        data) + "\r\n 【RESPONSE】:  " + str(result)
    return msg
