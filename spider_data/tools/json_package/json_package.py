def json_package(json_dict, element, status, base):
    if status == "0":
        e_value = json_dict[element]
        base[element] = str(e_value).replace('"', "").replace("'", "")
    elif status == "1":
        if element in json_dict:
            e_value = json_dict[element]
            base[element] = str(e_value).replace('"', "").replace("'", "")
    else:
        if element in json_dict:
            e_value = json_dict[element]
            base[element] = str(e_value).replace('"', "").replace("'", "")
        else:
            base[element] = json_dict.setdefault(element, "")

    return base


def json_package_update(json_dict, element, status):
    base = {}
    if status == "0":
        e_value = json_dict[element]
        base[element] = str(e_value).replace('"', "").replace("'", "")
    elif status == "1":
        if element in json_dict:
            e_value = json_dict[element]
            base[element] = str(e_value).replace('"', "").replace("'", "")
    else:
        if element in json_dict:
            e_value = json_dict[element]
            base[element] = str(e_value).replace('"', "").replace("'", "")
        else:
            base[element] = json_dict.setdefault(element, "")

    return base


def json_None(json_dict, element, status, base):
    if status == "0":
        e_value = json_dict[element]
        base[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "")
    elif status == "1":
        if element in json_dict:
            e_value = json_dict[element]
            base[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "")
    else:
        if element in json_dict:
            e_value = json_dict[element]
            base[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "")
        else:
            base[element] = json_dict.setdefault(element, "")

    return base
