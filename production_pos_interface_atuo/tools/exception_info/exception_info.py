ex_strg = "None"


def set_exception_info(ex_str):
    global ex_strg
    ex_strg = ex_str


def get_exception_info():
    return ex_strg
