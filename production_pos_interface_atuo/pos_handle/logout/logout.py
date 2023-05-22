from tools.params.params_requests_handle import params_requests_handle
from tools.decorfun import fun_info_name
from tools.login_cache.login_cache import get_login_cahe


@fun_info_name("POS:退出登录")
def logout():
    method = "test.git.hub.from.tars.logout"
    params = {
        "ctx_id": get_login_cahe().get("ctx_id"),
        "line_ai": "true"
    }
    params_requests_handle(method, params)
