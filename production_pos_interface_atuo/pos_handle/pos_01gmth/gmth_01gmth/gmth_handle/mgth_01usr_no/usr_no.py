from tools.params.params_requests_handle import params_requests_handle
from tools.sub_unit_num_id import get_sub_unit_num_id


def usr_no():
    method = "gb.member.pos.member.info.get"
    params = {
        "usr_no": "13100000000",
        "sub_unit_num_id": get_sub_unit_num_id().get("sub_unit_num_id"),
        "line_ai": "true"
    }
    return params_requests_handle(method, params)


def get_use_no_data():
    res = usr_no()
    return res["usr_num_id"], res["available_integral"], res["vip_type_num_id"], res["usr_name"], res["mobile_phone"], \
           res["card_no"]
