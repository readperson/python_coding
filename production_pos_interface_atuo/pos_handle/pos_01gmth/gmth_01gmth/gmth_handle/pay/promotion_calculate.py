from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.pay.pay_check import pay_check
from tools.tml_num_id import get_tml_num_id
from tools.params.params_requests_handle import params_requests_handle
from tools.user_id import set_user_id


def promotion_calculate():
    pay_check()
    method = "gb.unitepos.sale.order.promotion.calculate"
    params = {
        "tml_num_id": get_tml_num_id().get("tml_num_id"),
        "line_ai": "true",
        "record_num_id": get_tml_num_id().get("tml_num_id")
    }
    res = params_requests_handle(method, params)
    set_user_id(res["tml_dtls"][0]["create_user_id"])
