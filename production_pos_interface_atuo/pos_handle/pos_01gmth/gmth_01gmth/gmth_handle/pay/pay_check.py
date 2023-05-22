from tools.params.params_requests_handle import params_requests_handle
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.tml_client_id.tml_client_id import get_tml_client_id
from tools.sub_unit_num_id import get_sub_unit_num_id
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.mgth_02searchgoods.searchgoods import searchgoods
from tools.tml_num_id import get_tml_num_id


def pay_check():
    searchgoods()
    method = "gb.unitepos.sale.tml.for.pay.check"
    params = {
        "tml_num_id": get_tml_num_id().get("tml_num_id"),
        "sub_unit_num_id": get_sub_unit_num_id().get("sub_unit_num_id"),
        "tml_client_id": get_tml_client_id(),
        "line_ai": "true"
    }
    params_requests_handle(method, params)
