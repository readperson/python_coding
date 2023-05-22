import sys
from tools.file_system_path import file_system_path

sys.path.append(file_system_path())
from tools.get_time import getNowTime
from api.requests_api import request_post_login
from tools.params.params_handle import params_handle
from tools.file_system_path import file_system_path
from tools.get_time import now_timestamp
from tools.login_cache.login_cache import set_login_cache
from tools.decorfun import fun_info_name
from tools.sub_unit_num_id import set_sub_unit_num_id
from tools.testing_name import set_testing_name

file_ctx_id_salt_path = file_system_path() + '/pos_handle/login/timestamp.txt'


def timestamp_login(loginname, password, url, login_interval, testing_name):
    set_testing_name(testing_name)
    with open(file_ctx_id_salt_path, "r", encoding="utf-8") as f:
        s_s = f.read().split(",")
        ctx_id = s_s[0]
        salt = s_s[1]
        old_timestamp = s_s[2]
        sub_unit_num_id = s_s[3]
        if login_interval is None:
            login_interval = 0
        login_interval = int(login_interval) * 60
    if now_timestamp() - int(old_timestamp) >= login_interval:
        ctx_id, salt, sub_unit_num_id = login(loginname, password, url, testing_name)
    set_login_cache(ctx_id, salt)
    set_sub_unit_num_id(sub_unit_num_id)


@fun_info_name("POS:登录")
def login(loginname, password, url, testing_name):
    '''
    url, data, method, params
    :return:
    '''

    params = {
        "client_version": "1.0.0.81",
        "testing_name": testing_name,
        "password": password,
        "login_name": loginname,
        "channel_num_id": "1",
        "line_ai": "true"
    }
    params = params_handle(params)
    method = "test.git.hub.from.tars.login"
    timestamp = getNowTime()
    data = "app_key=12000&timestamp=" + str(timestamp) + "&method=" + method + "&sign=&params=" + params
    result = request_post_login(url, data, method, params)
    with open(file_ctx_id_salt_path, "w", encoding="utf-8") as f:
        f.write(result["ctx_id"] + "," + result["salt"] + "," + str(now_timestamp()) + "," + str(
            result["user_session"]["sub_unit_num_id"]))
    return result["ctx_id"], result["salt"], result["user_session"].get("sub_unit_num_id")


if __name__ == '__main__':
    login("testing_usernam", "123321", "http://postest.testting.com/testing")
