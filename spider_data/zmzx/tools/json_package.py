import sys

sys.path.append("/opt/data_captureAPP")
def json_package(json_dict, element, status, base):
    # result["comment_list"][c_count], "id", "", comment_dict
    if status == "0":
        e_value = json_dict[element]
        if element == "id":
            element = "pkey"
        base[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace("False", "")
    elif status == "1":
        if element in json_dict:
            e_value = json_dict[element]
            if element == "id":
                element = "pkey"
            base[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace("False", "")
    else:
        if element in json_dict:
            e_value = json_dict[element]
            if element == "id":
                element = "pkey"
            base[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace("False", "")
        else:
            base[element] = json_dict.setdefault(element, "")

    return base
