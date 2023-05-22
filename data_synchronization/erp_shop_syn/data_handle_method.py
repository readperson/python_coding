from tools.file_system_path import file_system_path


def data_handle(cursor_source, cursor_target, item_num_id, item_num_id_temp, style_num_id):
    '''
    :param cursor_source:
    :param cursor_target:
    :param item_num_id:
    :return:
    '''
    # 读取表信息
    with open(file_system_path() + "/tools/tables_config/tables_config.txt", "r", encoding="utf-8") as f:
        tables = f.readlines()
        for table_str in tables:
            table_str = table_str.replace("\n", "")
            table_name = table_str.split("@^A")[0]
            table_id = table_str.split("@^A")[1]
            # 处理ID问题
            if table_id == "style_num_id":
                item_num_id = style_num_id
            else:
                item_num_id = item_num_id_temp

            # 目标端：查询联合主键
            # show index from ustyss_p_channel_oprytd_shop where Non_unique =0 and Key_name <> 'PRIMARY'
            cursor_target.execute("show index from " + table_name + " where Non_unique =0 and Key_name <> 'PRIMARY'")
            uq_lists = cursor_target.fetchall()

            # 源端：获取表的数据
            cursor_source.execute("select * from " + table_name + " where  " + table_id + "=%s", item_num_id)
            ustyss_p_channel_oprytd_shop_list = cursor_source.fetchall()
            str_info2 = "正在同步【" + table_name + "】表"
            print(str_info2.center(100, "*"))
            # 源端：组装数据
            for channle_shop_index in range(len(ustyss_p_channel_oprytd_shop_list)):

                # 组装联合主键查询SQL
                qu_str = ''
                qu_count = 0
                for qu_list in uq_lists:
                    qu_count += 1
                    column_value = ustyss_p_channel_oprytd_shop_list[channle_shop_index].get(qu_list.get("Column_name"))
                    if qu_count == len(uq_lists):
                        qu_str = qu_str + qu_list.get("Column_name") + "='" + str(column_value) + "'"
                    else:
                        qu_str = qu_str + qu_list.get("Column_name") + "='" + str(column_value) + "' and "
                # 表字段
                keys = []
                # 表数据
                values = []
                # 占位符
                s = []
                # 源端：组装插入数据
                for channle_shop_key, channle_shop_value in ustyss_p_channel_oprytd_shop_list[
                    channle_shop_index].items():
                    keys.append(channle_shop_key)
                    values.append(channle_shop_value)
                    s.append("%s")

                # 源端：组装修改数据数据（字段）
                str_key = ""
                for index in range(len(keys)):
                    if keys[index] == "series":
                        continue
                    if len(keys) - 1 == index:
                        str_key = str_key + "" + keys[index] + "='" + str(values[index]) + "'"
                    else:
                        str_key = str_key + "" + keys[index] + "='" + str(values[index]) + "',"

                # 源端： 处理插入数据
                # 列
                insrt_keys = str(keys).replace("'", '').replace("[", "(").replace("]", ")")
                # 占位符
                inser_s = str(s).replace("'", '').replace("[", "(").replace("]", ")")
                # 目标端：查询目标端联合主键
                if len(uq_lists) > 0:
                    # 有联合主键执行的操作
                    cursor_target.execute("select * from " + table_name + " where  " + qu_str + "")
                else:
                    # 没有联合主键执行的操作
                    qu_str = "item_num_id = '" + item_num_id + "'"
                    cursor_target.execute("select * from " + table_name + " where  " + qu_str + "")
                # 目标端：获取返回数据
                ustyss_p_channel_oprytd_shop_target_list = cursor_target.fetchall()

                # 目标端：没有查询到数据 进入新增操作
                if len(ustyss_p_channel_oprytd_shop_target_list) < 1:

                    # 目标端：查询series数据
                    ser_str = "series='" + str(values[0]) + "'"
                    sql_query = "select * from " + table_name + " where " + ser_str
                    cursor_target.execute(sql_query)
                    series_list = cursor_target.fetchall()
                    # 防止主键冲突 需要确认series数据是否存在
                    if len(series_list) > 0:
                        # 如果series有数据就更新整个条记录
                        str_info5 = "执行【" + table_name + "】表修改一操作"
                        print(str_info5.center(100, "*"))
                        sql_update = "update " + table_name + " set " + str_key.replace("'None'", "Null") + \
                                     " where series ='" + str(series_list[0]["series"]) + "'"
                        cursor_target.execute(sql_update)
                    # series主键未查到数据 执行新增操作
                    else:
                        str_info3 = "执行【" + table_name + "】表新增操作"
                        print(str_info3.center(100, "*"))
                        cursor_target.execute("insert into " + table_name + " " + insrt_keys +
                                              " value " + inser_s + "", values)
                # 目标端有数据就修改
                else:
                    str_info4 = "执行【" + table_name + "】表修改二操作"
                    print(str_info4.center(100, "*"))
                    sql_update = "update " + table_name + " set " + str_key.replace("'None'", "Null") + \
                                 " where " + qu_str
                    cursor_target.execute(sql_update)
                print("")
