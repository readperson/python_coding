import pymysql
from erp_shop_syn.data_handle_method import data_handle
from erp_shop_syn.conn_source.conn_source import con_source
from erp_shop_syn.conn_target.conn_target import con_target
from tools.erp_tools_method import table_basic_read
from tools.erp_tools_method import save_erp_shop_info
from tools.get_time import get_now_time_underline
from tools.file_system_path import file_system_path
from tools.logconfig.logingconfig import loging
from tools.operaexcel.operaExcel import OperaExcel


def syn_oprytd_data():
    try:
        # 源端数据连接
        nowtime = get_now_time_underline()
        conn_source = pymysql.connect(host=con_source()[0], port=int(con_source()[1]), user=con_source()[2],
                                      passwd=con_source()[3], db=con_source()[4],
                                      charset='utf8')
        cursor_source = conn_source.cursor(cursor=pymysql.cursors.DictCursor)
        # 目标端目标端数据连接
        conn_target = pymysql.connect(host=con_target()[0], port=int(con_target()[1]), user=con_target()[2],
                                      passwd=con_target()[3], db=con_target()[4],
                                      charset='utf8')
        cursor_target = conn_target.cursor(cursor=pymysql.cursors.DictCursor)
        # 源端：基表数量
        cursor_source.execute(
            "select count(*) from " + table_basic_read()[0] + " where length(" + table_basic_read()[1] + ") <" +
            table_basic_read()[2])
        ustyss_p_oprytd_basic_count = cursor_source.fetchall()[0]["COUNT0"]

        # 源端：查询源端基表
        # 从配置文件读取更新数据条数
        # cursor_source.execute(
        #     "select * from " + table_basic_read()[0] + " where length(" + table_basic_read()[1] + ") <" +
        #     table_basic_read()[2] + " limit " + table_basic_read()[3])
        # 从数据库中查询更新总记录数
        cursor_source.execute(
            "select * from " + table_basic_read()[0] + " where length(" + table_basic_read()[1] + ") <" +
            table_basic_read()[2] + " limit " + str(ustyss_p_oprytd_basic_count))
        # 源端：返回基表列表
        ustyss_p_oprytd_basic_list = cursor_source.fetchall()
        # 源端：循环列表数据
        for basic_index in range(len(ustyss_p_oprytd_basic_list)):
            # info_str = "本次同步数据" + str(table_basic_read()[3]) + "条,正在同步第" + str(basic_index + 1) + "条数据"
            info_str = "本次同步数据共计" + str(ustyss_p_oprytd_basic_count) + "条,正在同步第" + str(basic_index + 1) + "条数据"
            print(info_str.center(100, "*"))
            # # 源端：保存同步的基本信息
            basic_series = ustyss_p_oprytd_basic_list[basic_index].get("series")
            item_num_id = ustyss_p_oprytd_basic_list[basic_index].get("item_num_id")
            item_name = ustyss_p_oprytd_basic_list[basic_index].get("item_name")
            style_num_id = ustyss_p_oprytd_basic_list[basic_index].get("style_num_id")
            # 保存同步商品信息
            shop_ids = save_erp_shop_info(basic_series, item_num_id, item_name, style_num_id, nowtime)
            # 处理同步数据方法
            data_handle(cursor_source, cursor_target, shop_ids[0], shop_ids[0], shop_ids[1])
            conn_target.commit()
            conn_source.commit()
            str_info1 = "第" + str(basic_index + 1) + "条数据同步完成"
            print(str_info1.center(100, "*"))
            print()

    finally:
        print("关闭数据连接".center(100, "*"))
        if cursor_target != None:
            print("cursor_target_colse".center(100, "*"))
            cursor_target.close()
        if conn_target != None:
            print("conn_target_colse".center(100, "*"))
            conn_target.close()
        if cursor_source != None:
            print("cursor_source_colse".center(100, "*"))
            cursor_source.close()
        if conn_source != None:
            print("conn_source_colse".center(100, "*"))
            conn_source.close()


def syn_oprytd_associate():
    try:
        file_path = file_system_path() + "/tools/tables_config/data_syn.xlsx"
        # OperaExcel.clean_up(file_path, "D2", "D18")
        lineCount = OperaExcel.get_lines(file_path)
        OperaExcel.clean_up(file_path, "M2", "M" + str(lineCount))
        for line in range(lineCount - 1):
            line += 1
            con_source_host = OperaExcel.get_cell(file_path, line, 0)
            con_source_port = OperaExcel.get_cell(file_path, line, 1)
            con_source_user = OperaExcel.get_cell(file_path, line, 2)
            con_source_passwd = OperaExcel.get_cell(file_path, line, 3)
            con_source_db_name = OperaExcel.get_cell(file_path, line, 4)
            con_target_host = OperaExcel.get_cell(file_path, line, 5)
            con_target_port = OperaExcel.get_cell(file_path, line, 6)
            con_target_user = OperaExcel.get_cell(file_path, line, 7)
            con_target_passwd = OperaExcel.get_cell(file_path, line, 8)
            con_target_db_name = OperaExcel.get_cell(file_path, line, 9)
            table_name = OperaExcel.get_cell(file_path, line, 10)
            status = OperaExcel.get_cell(file_path, line, 11)
            time_word = str(OperaExcel.get_cell(file_path, line, 13))
            get_syn_time = str(OperaExcel.get_cell(file_path, line, 14))

            # with open(file_system_path() + "/tools/tables_config/oprytd_associate.txt", "r", encoding="utf-8") as f:
            #     read_lines = f.readlines()
            #     for read_line in read_lines:

            # db_name, table_name, status = str(read_line).replace('\n', '').split(":")
            if status == "Y":
                # 源端数据连接
                conn_source = pymysql.connect(host=con_source_host, port=con_source_port, user=con_source_user,
                                              passwd=con_source_passwd, db=con_source_db_name,
                                              charset='utf8')
                cursor_source = conn_source.cursor(cursor=pymysql.cursors.DictCursor)

                # 目标端数据连接
                conn_target = pymysql.connect(host=con_target_host, port=con_target_port, user=con_target_user,
                                              passwd=con_target_passwd, db=con_target_db_name,
                                              charset='utf8')
                cursor_target = conn_target.cursor(cursor=pymysql.cursors.DictCursor)

                # 判断表是否存在
                cursor_target.execute("show tables like '%" + table_name + "%'")

                target_tables_exits = cursor_target.fetchone()
                # 判断源端是否有该表
                if target_tables_exits is None:
                    # 如果源端没有表就创建
                    cursor_source.execute("show create table " + table_name)
                    create_table_source = cursor_source.fetchone()
                    cursor_target.execute(create_table_source['Create Table'])
                # 获取表总记录数
                if get_syn_time == "None":
                    cursor_source.execute("select count(*) from " + table_name)
                    source_count = cursor_source.fetchall()
                    source_sql_query = "select * from " + table_name + " limit " + str(source_count[0]["COUNT0"])
                    cursor_source.execute(source_sql_query)
                    # 获取表数据
                    source_lists = cursor_source.fetchall()
                else:

                    sql_count_query = "select count(0) from " + table_name + " where " + time_word + " >= '" + get_syn_time + "'"
                    cursor_source.execute(sql_count_query)
                    source_count = cursor_source.fetchall()
                    count_jl = list(source_count[0].values())[0]
                    source_sql_query = "select * from " + table_name + " where " + time_word + " >= '" + get_syn_time + "' limit " + str(count_jl)
                    print("source_sql_query2", source_sql_query)
                    cursor_source.execute(source_sql_query)
                    # 获取表数据
                    source_lists = cursor_source.fetchall()
                    print("source_lists2", len(source_lists))

                k_t = "数据库:【" + con_target_db_name + "】 表:【" + table_name + "】"

                loging("".center(100, "*"))
                loging(k_t.center(100, "*"))
                loging("".center(100, "*"))

                for source_query_index in range(len(source_lists)):

                    # cursor_target.execute("show index from ustyss_o_oprytd_origin  where Non_unique =0 and Key_name = 'PRIMARY'")
                    # 查询联合主键
                    cursor_target.execute(
                        "show index from " + table_name + " where Non_unique =0 and Key_name <> 'PRIMARY'")
                    uq_lists = cursor_target.fetchall()

                    # 处理联合主键
                    uq_count = len(uq_lists)
                    count = 0
                    uq_sql_str = ""
                    for uq_list in range(uq_count):
                        # 组装联合主键
                        count += 1
                        if uq_count == count:
                            uq_sql_str = uq_sql_str + "" + uq_lists[uq_list]["Column_name"] + " = '" + str(
                                source_lists[source_query_index][uq_lists[uq_list]["Column_name"]]) + "'"
                        else:
                            uq_sql_str = uq_sql_str + "" + uq_lists[uq_list]["Column_name"] + " = '" + str(
                                source_lists[source_query_index][uq_lists[uq_list]["Column_name"]]) + "' and "
                    cursor_target.execute(
                        "show index from " + table_name + "  where Non_unique =0 and Key_name = 'PRIMARY'")
                    cursor_target_primary = cursor_target.fetchall()
                    # 处理主键
                    primary_sql_str = cursor_target_primary[0]["Column_name"] + " = '" + str(
                        source_lists[source_query_index][cursor_target_primary[0]["Column_name"]]) + "'"

                    # 没有联合主键
                    if len(uq_lists) == 0:
                        target_sql_query = "select * from " + table_name + " where " + primary_sql_str
                    else:
                        # 有联合主键
                        target_sql_query = "select * from " + table_name + " where " + uq_sql_str

                    cursor_target.execute(target_sql_query)
                    target_lists = cursor_target.fetchone()

                    # 如果联合主键和主键没有查询到数据就新增
                    if target_lists is None:
                        # 组装插入
                        # print("插入数据".center(100, "*"))
                        insert_vlaues = []
                        for key, vlaue in source_lists[source_query_index].items():
                            insert_vlaues.append(str(vlaue))
                        insert_vlaues = str(insert_vlaues).replace("[", "(").replace("]", ")").replace("'None'",
                                                                                                       "Null")
                        insert_sql = "insert into " + table_name + " values " + insert_vlaues + ""
                        loging("插入数据:" + str(insert_sql))
                        cursor_target.execute(insert_sql)

                    else:
                        # 如果联合主键和主键查询到数据 在根据主键来查询
                        query_primary_sql = "select * from " + table_name + " where " + primary_sql_str
                        cursor_target.execute(query_primary_sql)
                        query_primary_list = cursor_target.fetchone()
                        if query_primary_list is not None:
                            # print("修改数据".center(100, "*"))
                            # 组装修改
                            update_sql_str = ""
                            update_count = 0
                            for key, vlaue in source_lists[source_query_index].items():
                                update_count += 1
                                if key == cursor_target_primary[0]["Column_name"]:
                                    continue
                                else:
                                    if update_count == len(source_lists[source_query_index].items()):
                                        # update_sql_str = update_sql_str + "" + key + "='" + str(vlaue) + "'"
                                        # print("update_sql_str", update_sql_str)
                                        update_sql_str = update_sql_str + '' + key + '="' + str(vlaue).replace('"',
                                                                                                               '\\"').replace(
                                            "'", "\\'") + '"'
                                    else:
                                        update_sql_str = update_sql_str + '' + key + '="' + str(vlaue).replace('"',
                                                                                                               '\\"').replace(
                                            "'", "\\'") + '",'

                            update_sql_target = "update " + table_name + " set " + update_sql_str.replace(
                                '"None"',
                                "Null") + " where " + primary_sql_str
                            loging("修改数据:" + str(update_sql_target))
                            cursor_target.execute(update_sql_target)
                        else:
                            # print("修改插入数据".center(100, "*"))
                            # 组装插入
                            insert_vlaues = []
                            for key, vlaue in source_lists[source_query_index].items():
                                insert_vlaues.append(str(vlaue))
                            insert_vlaues = str(insert_vlaues).replace("[", "(").replace("]", ")").replace("'None'",
                                                                                                           "Null")
                            insert_sql = "insert into " + table_name + " values " + insert_vlaues + ""
                            loging("修改插入数据:", str(insert_sql))
                            cursor_target.execute(insert_sql)

                conn_target.commit()
                conn_source.commit()
                # is_run = OperaExcel.get_cell(file_path, line, 3)
                OperaExcel.save_run_result(line + 1, 12, file_path)
                OperaExcel.save_data_syn(line + 1, 15, file_path)
                k_end = "数据库:【" + con_target_db_name + "】 表:【" + table_name + "】同步完成"
                loging(k_end.center(100, "*"))


            else:
                k_t = "无需同步数据库:【" + con_target_db_name + "】 表:【" + table_name + "】数据"

                loging("".center(100, "*"))
                loging(k_t.center(100, "*"))
                loging("".center(100, "*"))
                loging("")
    # except Exception as e:
    #     print(e)
    #
    #     loging("执行出现异常")

    finally:
        loging("关闭数据连接".center(100, "*"))
    if cursor_target != None:
        loging("cursor_target_colse".center(100, "*"))
        cursor_target.close()
    if conn_target != None:
        loging("conn_target_colse".center(100, "*"))
        conn_target.close()
    if cursor_source != None:
        loging("cursor_source_colse".center(100, "*"))
        cursor_source.close()
    if conn_source != None:
        loging("conn_source_colse".center(100, "*"))
        conn_source.close()


if __name__ == '__main__':
    syn_oprytd_associate()
    # syn_oprytd_data()
