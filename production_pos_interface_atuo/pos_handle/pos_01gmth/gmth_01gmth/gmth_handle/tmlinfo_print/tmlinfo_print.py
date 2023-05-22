from tools.tml_num_id import get_tml_num_id
from tools.params.params_requests_handle import params_requests_handle
from tools.decorfun import fun_info_name


@fun_info_name("POS:购买商品,打印小票")
def tmlinfo_print():
    method = "gb.unitepos.sale.tmlinfo.print"
    params = {
        "tml_num_id": get_tml_num_id().get("tml_num_id"),
        "line_ai": "true"
    }
    params_requests_handle(method, params)
