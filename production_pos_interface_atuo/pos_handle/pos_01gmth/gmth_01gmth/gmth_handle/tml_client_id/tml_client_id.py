from tools.params.params_requests_handle import params_requests_handle
from tools.sub_unit_num_id import get_sub_unit_num_id
from tools.testing_name import get_testing_name


def tml_client_id():
    method = "test.git.hub.tars.forcash.prepare"
    params = {
        "testing_name": get_testing_name().get("testing_name"),
        "sub_unit_num_id": get_sub_unit_num_id().get("sub_unit_num_id"),
        "page_id": "e547f23e4c8740b1b90a14b495f68904",
        "line_ai": "true"
    }
    return params_requests_handle(method, params)


def get_tml_client_id():
    return tml_client_id()["tml_client_id"]
