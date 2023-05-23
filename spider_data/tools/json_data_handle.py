from tools.base64_text import text_conversion_base64


def data_lens(datas):
    '''
    返回json数据长度
    '''
    data_count = int(len(datas))
    return data_count


def json_mapping(json_element, element, status, base_dict):
    '''
    对json文件进行映射处理返回base_dict字典
    :param json_element:
    :param element:
    :param status:
    :param base_dict:
    :return: base_dict
    '''
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
            # base64编码处理
            if basels[1] == "base64":
                # 处理 KeyError:
                if basels[0] in json_element:
                    e_value = json_element[basels[0]]
                    base_dict[basels[0]] = text_conversion_base64(e_value)
                else:
                    base_dict[basels[0]] = json_element.setdefault(basels[0], "")
            # 特殊字符处理只保留数字、字母和汉字

            else:
                print("✘等式解析异常,注意分割符数据~~~~")
                raise Exception

        elif element in json_element:
            e_value = json_element[element]
            if element == "id":
                element = "pkey"
            base_dict[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace("False", "")
        else:
            base_dict[element] = json_element.setdefault(element, "")

    return base_dict


def json_data_handle(json_dict, data_c, list_dict):
    '''
    :param json_dict:
    :param data_c:
    :param list_dict:
    :return:
    '''
    j_dict = {}
    for list_d in list_dict:
        json_mapping(json_dict[data_c], list_d, "", j_dict)
    return j_dict


def json_data_handle_single(json_dict, list_dict):
    '''
    :param json_dict:
    :param data_c:
    :param list_dict:
    :return:
    '''
    j_dict = {}
    for list_d in list_dict:
        json_mapping(json_dict, list_d, "", j_dict)
    return j_dict
