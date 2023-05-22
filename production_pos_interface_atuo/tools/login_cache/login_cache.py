ctx_id_salt = {}
login_domian = {}


def set_login_cache(ctx_id, salt):
    ctx_id_salt["ctx_id"] = ctx_id
    ctx_id_salt["salt"] = salt


def get_login_cahe():
    return ctx_id_salt
