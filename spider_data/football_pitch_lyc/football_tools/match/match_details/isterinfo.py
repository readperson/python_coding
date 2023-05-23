def isterinfo(isterInfo):
    res_count = int(len(isterInfo))
    isterInfo_list = []
    for r_cont in range(res_count):
        isterInfo_dict = {}
        json_package(isterInfo[r_cont], "playerId", "", isterInfo_dict)
        json_package(isterInfo[r_cont], "coordinateX", "", isterInfo_dict)
        json_package(isterInfo[r_cont], "coordinateY", "", isterInfo_dict)
        json_package(isterInfo[r_cont], "isFirst", "", isterInfo_dict)
        json_package(isterInfo[r_cont], "portrait", "", isterInfo_dict)
        json_package(isterInfo[r_cont], "username", "", isterInfo_dict)
        json_package(isterInfo[r_cont], "memberNumber", "", isterInfo_dict)
        json_package(isterInfo[r_cont], "faceImg", "", isterInfo_dict)
        json_package(isterInfo[r_cont], "isSuspend", "", isterInfo_dict)
        isterInfo_dict["faceImg"] = ""
        isterInfo_dict["portrait"] = ""
        isterInfo_list.append(isterInfo_dict)
    return isterInfo_list


def json_package(json_dict, element, status, base):
    if status == "0":
        e_value = json_dict[element]
        base[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace(" ", "")
    elif status == "1":
        if element in json_dict:
            e_value = json_dict[element]
            base[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace(" ", "")

    else:
        if element in json_dict:
            e_value = json_dict[element]
            base[element] = str(e_value).replace('"', "").replace("'", "").replace("None", "").replace(" ", "")

        else:
            base[element] = json_dict.setdefault(element, "")

    return base
