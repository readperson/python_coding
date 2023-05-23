from tools.base64_text import text_conversion_base64


def data_lens(datas):
    data_count = int(len(datas))
    return data_count


def json_mapping(json_element, element, status, base_dict):
    if status == "0":
        e_value = json_element[element]
        if element == "id":
            element = "pkey"

        base_dict[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace("False", "")
    elif status == "1":
        if element in json_element:
            e_value = json_element[element]
            if element == "id":
                element = "pkey"
            base_dict[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace("False", "")
    else:
        if element.find("=") != -1:
            basels = element.split("=")
            if basels[1] == "base64":
                # e_value = json_element[basels[0]]
                # 处理 KeyError: 'description'
                if basels[0] in json_element:
                    e_value = str(json_element[basels[0]]).replace(
                        "广州动因", "篮球约").replace("动因", "篮球约").replace("广州", "篮球约")
                    base_dict[basels[0]] = text_conversion_base64(e_value)
                else:
                    base_dict[basels[0]] = json_element.setdefault(basels[0], "")

            else:
                print("等式解析异常注意分割符~~~~")
                raise Exception

        elif element in json_element:
            e_value = json_element[element]
            if element == "id":
                element = "pkey"
            base_dict[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace("False",
                                                                                                            "").replace(
                "广州动因", "篮球约").replace("动因", "篮球约").replace("广州","篮球约")
        else:
            base_dict[element] = json_element.setdefault(element, "")

    return base_dict


def json_data_handle(json_dict, data_c, list_dict):
    j_dict = {}
    for list_d in list_dict:
        json_mapping(json_dict[data_c], list_d, "", j_dict)
    return j_dict
