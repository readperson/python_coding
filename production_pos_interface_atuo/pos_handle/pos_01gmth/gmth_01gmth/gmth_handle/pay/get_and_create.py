from tools.params.params_requests_handle import params_requests_handle
from tools.tml_num_id import get_tml_num_id
from tools.sub_unit_num_id import get_sub_unit_num_id
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.tml_client_id.tml_client_id import get_tml_client_id
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.pay.promotion_calculate import promotion_calculate
from tools.pay_amount import set_pay_amount


def get_and_create():
    '''
    预付款成功
    :return:
    '''
    promotion_calculate()
    method = "gb.unitepos.sale.cash.pay.hdr.get.and.create"
    params = {
        "sub_unit_num_id": get_sub_unit_num_id().get("sub_unit_num_id"),
        "tml_num_id": get_tml_num_id().get("tml_num_id"),
        "ef_amount": "0",
        "ist_amount": "0",
        "tml_client_id": get_tml_client_id(),
        "line_ai": "true"
    }
    res = params_requests_handle(method, params)
    p_amount = res.get("tml_pay_hdr").get("p_amount")
    set_pay_amount(p_amount)
