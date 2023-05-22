from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.tml_client_id.tml_client_id import get_tml_client_id
from pos_handle.pos_01gmth.gmth_01gmth.tuihuo.refund_create import get_tml_num_id
from tools.params.params_requests_handle import params_requests_handle


def pay_create_refund():
    method = "gb.unitepos.sale.cash.pay.hdr.get.and.create.refund"
    params = {
        "tml_num_id": get_tml_num_id(),
        "tml_client_id": get_tml_client_id(),
        "line_ai": "true"
    }
    return params_requests_handle(method, params)


def get_data():
    res = pay_create_refund()
    return res.get("source_cash_dtls")[0].get("pay_amount"), res.get("source_cash_dtls")[0].get("reserved_no"), res.get(
        "tml_pay_hdr").get("tml_num_id")
