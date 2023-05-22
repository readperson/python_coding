from tools.file_system_path import file_system_path


def con_target():
    with open(file_system_path() + "/erp_shop_syn/conn_target/conn_target.txt", "r", encoding="utf-8")as f:
        conn_source = f.read()
        return conn_source.split(",")[0], conn_source.split(",")[1], conn_source.split(",")[2], conn_source.split(",")[
            3], conn_source.split(",")[4]


