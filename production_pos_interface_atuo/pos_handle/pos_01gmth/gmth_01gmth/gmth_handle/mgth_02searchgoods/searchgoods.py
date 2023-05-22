from tools.params.params_requests_handle import params_requests_handle
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.handover_id.get_handover_id import get_handover_id
from tools.sub_unit_num_id import get_sub_unit_num_id
import random
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.mgth_01usr_no.usr_no import get_use_no_data
from tools.get_time import get_now_time_y_m_d
from tools.tml_num_id import set_tml_num_id
from tools.item_name import set_item_name
from tools.goods import get_goods


def searchgoods():
    method = "gb.cexport.data.export"
    params = {
        "sql_id": "POS-XDL-search-oprytd-by-name-like",
        "page_size": "200",
        "page_num": "1",
        "input_param": {
            "item_name": get_goods(),
            "sub_unit_num_id": get_sub_unit_num_id().get("sub_unit_num_id")
        },
        "line_ai": "true"
    }
    res = params_requests_handle(method, params)["results"]
    barcode = res[random.randint(0, len(res) - 1)]["barcode"]

    method = "gb.unitepos.sale.order.tml.hdr.and.dtl.create"
    usr_num_id, last_point, vip_type, usr_name, usr_tel, vip_no = get_use_no_data()
    params = {
        "type_num_id": "1",
        "so_from_type": "1",
        "settlement_type_id": "1",
        "handover_id": get_handover_id(),
        # 线下 90
        "channel_num_id": "90",
        "barcode": barcode,
        "usr_num_id": usr_num_id,
        "practice_type": "0",
        "last_point": last_point,
        "vip_type": vip_type,
        "usr_name": usr_name,
        "usr_tel": usr_tel,
        "vip_no": vip_no,
        "sale_date": get_now_time_y_m_d(),
        "is_tm": "0",
        "client_type_num_id": "0",
        "is_check_tran_type": "0",
        "integral_plus_sign": "0",
        "line_ai": "true"
    }
    res = params_requests_handle(method, params)
    set_tml_num_id(res["tml_num_id"])
    set_item_name(res["item_name"])
