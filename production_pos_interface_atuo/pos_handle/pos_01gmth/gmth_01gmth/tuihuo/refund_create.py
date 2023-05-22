from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.handover_id.get_handover_id import get_handover_id
from pos_handle.pos_01gmth.gmth_01gmth.tuihuo.tml_get import tml_get
from tools.params.params_requests_handle import params_requests_handle


def refund_create():
    type_num_id, so_from_type, settlement_type_id, source_tml_num_id, barcode, source_tml_line, qty = tml_get()
    method = "com.gb.soa.omp.sale.order.refund.create"
    params = {
        "back_reason": "",
        "practice_type": "0",
        "type_num_id": "2",
        "so_from_type": str(so_from_type),
        "settlement_type_id": str(settlement_type_id),
        "handover_id": str(get_handover_id()),
        "channel_num_id": "90",
        "remark": "",
        "refund_possess_origin_tml_flag": "1",
        "source_tml_num_id": source_tml_num_id,
        "tml_num_id": "0",
        "tars_return_items": [
            {
                "barcode": barcode,
                "source_tml_line": source_tml_line,
                "qty": str(qty)
            }
        ],
        "line_ai": "true",
        "permission_id": "59874a7a7e7049669e95b9cf90de75ae"
    }
    return params_requests_handle(method, params)


def get_tml_num_id():
    return refund_create().get("tml_num_id")
