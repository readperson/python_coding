user_id_dict = {}


def set_user_id(user_id):
    user_id_dict["user_id"] = user_id


def get_user_id():
    return user_id_dict.get("user_id")
