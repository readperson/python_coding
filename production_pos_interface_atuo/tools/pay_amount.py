pay_amount_dict = {}


def set_pay_amount(pay_amount):
    pay_amount_dict["pay_amount"] = pay_amount


def get_pay_amount():
    return pay_amount_dict.get("pay_amount")
