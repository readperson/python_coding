from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.handover_id.get_handover_id import get_handover_id
from tools.user_id import get_user_id
from tools.params.params_requests_handle import params_requests_handle
from tools.decorfun import fun_info_name


@fun_info_name("POS:交班")
def handover():
    handover_id = get_handover_id()
    user_num_id = get_user_id()
    method = "gb.unitepos.sale.handoverdtl.get"
    params = {
        "handover_id": handover_id,
        "user_num_id": user_num_id,
        "line_ai": "true"
    }
    amount = params_requests_handle(method, params).get("check_all_amount")

    method = "gb.unitepos.sale.cash.tars.cash.handover"
    params = {
        "user_num_id": user_num_id,
        "handover_id": handover_id,
        "amount": amount,
        "auto_sign": "0",
        "line_ai": "true",
        "permission_id": "7e4b8f1df6414667a6a6a50f88fac5ca"
    }
    params_requests_handle(method, params)
