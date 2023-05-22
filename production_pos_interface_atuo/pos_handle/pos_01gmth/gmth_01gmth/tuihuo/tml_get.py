from tools.params.params_requests_handle import params_requests_handle
from tools.tml_num_id import get_tml_num_id
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.handover_id.get_handover_id import get_handover_id
import random


def tml_get():
    method = "com.gb.soa.omp.sale.order.refund.origin.tml.get"
    params = {
        "cross_return_sign": "0",
        "practice_type": "0",
        "tml_num_id": get_tml_num_id().get("tml_num_id"),
        "handover_id": get_handover_id(),
        "line_ai": "true",
        "permission_id": "59874a7a7e7049669e95b9cf90de75ae"
    }
    res = params_requests_handle(method, params)
    return res["hdr"].get("type_num_id"), res["hdr"].get("so_from_type"), res["hdr"].get("settlement_type_id"), \
           res["dtl_list"][0].get("tml_num_id"), res["dtl_list"][0].get("barcode"), res["dtl_list"][0].get("series"), \
           res["dtl_list"][0].get("qty")
