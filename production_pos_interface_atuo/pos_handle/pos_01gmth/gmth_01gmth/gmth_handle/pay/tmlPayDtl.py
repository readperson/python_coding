from tools.params.params_requests_handle import params_requests_handle
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.pay.get_and_create import get_and_create
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.tml_client_id.tml_client_id import get_tml_client_id
from tools.tml_num_id import get_tml_num_id
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.handover_id.get_handover_id import get_handover_id
from tools.item_name import get_item_name
from tools.pay_amount import get_pay_amount
from tools.decorfun import fun_info_name


@fun_info_name("POS:购买商品")
def tmlPayDtl():
    """
    付款
    :return:
    """
    get_and_create()
    method = "com.gb.soa.omp.ccash.api.service.CashDtlService.tmlPayDtl"
    params = {
        "tml_client_id": get_tml_client_id(),
        "tml_num_id": get_tml_num_id().get("tml_num_id"),
        "pay_amount": get_pay_amount(),
        "pay_type_id": "0",
        "handover_id": get_handover_id(),
        "card_type_id": "0",
        "app_key": "12000",
        "auth_code": "",
        "body": get_item_name().get("item_name") + "等",
        "m_amount": "0",
        "line_ai": "true"
    }
    params_requests_handle(method, params)
