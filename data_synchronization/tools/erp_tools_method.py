from tools.file_system_path import file_system_path


def table_basic_read():
    with open(file_system_path() + "/tools/tables_config/table_basic.txt", "r", encoding="utf-8") as f:
        basic_str = f.read()
        return basic_str.split("@^A")[0], basic_str.split("@^A")[1], basic_str.split("@^A")[2], basic_str.split("@^A")[
            3]


def save_erp_shop_info(basic_series, item_num_id, item_name, style_num_id, nowtime):
    # 源端：保存基本信息
    basic_series = str(basic_series).replace('[', '').replace(']', '')
    item_num_id = str(item_num_id).replace('[', '').replace(']', '')
    item_name = str(item_name).replace('[', '').replace(']', '')
    style_num_id = str(style_num_id).replace('[', '').replace(']', '')
    #
    with open(file_system_path() + "/tools/erp_shop_info/" + nowtime + "_shopinfo.txt", "a+", encoding="utf-8") as f:
        f.write(
            "basic_series:" + basic_series + ",item_num_id:" + item_num_id + ",item_name:" + item_name + ",style_num_id:" + style_num_id + "\n")

    return item_num_id, style_num_id
