from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.handover_id.get_handover_id import get_handover_id
from pos_handle.pos_01gmth.gmth_01gmth.tuihuo.pay_create_refund import get_data
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.tml_client_id.tml_client_id import get_tml_client_id
from tools.params.params_requests_handle import params_requests_handle
from tools.decorfun import fun_info_name
from tools.logconfig.logingconfig import loging


@fun_info_name("POS:退货")
def refundTmlPayForPos():
    pay_amount, source_tml_num_id, tml_num_id, = get_data()
    method = "gb.unitepos.sale.cash.pay.refundTmlPayForPos"
    params = {
        "app_key": "12000",
        "card_type_id": "0",
        "handover_id": get_handover_id(),
        "pay_amount": pay_amount,
        "pay_type_id": "0",
        "source_tml_num_id": source_tml_num_id,
        "tml_client_id": get_tml_client_id(),
        "tml_num_id": tml_num_id,
        "line_ai": "true"
    }

    res = params_requests_handle(method, params)
    loging("POS:退货小票打印".center(50, "*"))
    tml_num_id = res.get("sd_bl_so_tml_pay_hdr").get("tml_num_id")
    method = "gb.unitepos.sale.tmlinfo.print"
    parmas = {
        "tml_num_id": tml_num_id,
        "line_ai": "true"
    }
    params_requests_handle(method, parmas)
