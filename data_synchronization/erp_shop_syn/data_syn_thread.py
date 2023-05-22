import pymysql
from tools.file_system_path import file_system_path
from tools.logconfig.logingconfig import loging
from tools.operaexcel.operaExcel import OperaExcel
from concurrent.futures import ThreadPoolExecutor
import math
import traceback
from tools.except_fun import except_fun
from tools.get_time import now_timestamp


def task(args):
    try:
        con_source_host, con_source_port, con_source_user, con_source_passwd, con_source_db_name, con_target_host, con_target_port, \
        con_target_user, con_target_passwd, table_name, con_target_db_name, time_word, get_syn_time, count_int, poolcount, pagesize = args
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

        # 查询联合主键
        cursor_target.execute(
            "show index from " + table_name + " where Non_unique =0 and Key_name <> 'PRIMARY'")
        uq_lists = cursor_target.fetchall()
        uq_count = len(uq_lists)
        # 表主键
        cursor_target.execute(
            "show index from " + table_name + "  where Non_unique =0 and Key_name = 'PRIMARY'")
        cursor_target_primary = cursor_target.fetchall()

        pagesize_limit = "limit " + str((pagesize - 1) * count_int) + "," + str(count_int)
        source_sql_query = "select * from " + table_name + " where " + time_word + " >= '" + str(
            get_syn_time) + "' " + pagesize_limit
        # print("执行查询sql:", source_sql_query)
        cursor_source.execute(source_sql_query)
        # 获取表数据
        source_lists = cursor_source.fetchall()

        k_t = "数据库:【" + con_target_db_name + "】 表:【" + table_name + "】 线程" + str(pagesize) + "启动"
        loging(k_t.center(100, "*"))

        for source_query_index in range(int(len(source_lists))):

            # 处理联合主键
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

            # 处理主键
            primary_sql_str = cursor_target_primary[0]["Column_name"] + " = '" + str(
                source_lists[source_query_index][cursor_target_primary[0]["Column_name"]]) + "'"

            # 没有联合主键
            if len(uq_lists) == 0:
                target_sql_query = "select * from " + table_name + " where " + primary_sql_str
            else:
                # 有联合主键
                target_sql_query = "select * from " + table_name + " where " + uq_sql_str

            # 联合主键查询
            cursor_target.execute(target_sql_query)
            target_lists = cursor_target.fetchone()
            # 主键查询
            query_primary_sql = "select * from " + table_name + " where " + primary_sql_str
            cursor_target.execute(query_primary_sql)
            query_primary_list = cursor_target.fetchone()

            if target_lists is not None:
                if query_primary_list is not None:
                    loging("总线程" + str(poolcount) + "_第" + str(pagesize) + "个正在执行,联合主键：" + str(
                        target_lists) + " 主键：" + str(query_primary_list) + "")
                    continue

            # 如果联合主键和主键没有查询到数据就新增
            if target_lists is None:
                if query_primary_list is None:
                    # 组装插入
                    insert_vlaues = []
                    for key, vlaue in source_lists[source_query_index].items():
                        insert_vlaues.append(str(vlaue))
                    insert_vlaues = str(insert_vlaues).replace("[", "(").replace("]", ")").replace("'None'", "Null")
                    insert_sql = "insert into " + table_name + " values " + insert_vlaues + ""
                    cursor_target.execute(insert_sql)
                    conn_target.commit()
                    loging("插入数据: 联合主键：" + str(target_lists) + " 主键：" + str(query_primary_list) + ",总线程" +
                           str(poolcount) + "_第" + str(pagesize) + "个正在执行 " + str(insert_sql))

        conn_close(conn_target, conn_source)
        str_end = "第" + str(pagesize) + "个线程结束"
        loging(str_end.center(100, "*"))
    except Exception as e:
        execpt_start = "线程" + str(pagesize) + "：异常信息: " + str(e) + "start"
        loging(execpt_start.center(100, "--"))
        parmas = [con_source_host, con_source_port, con_source_user, con_source_passwd, con_source_db_name, \
                  con_target_host, con_target_port, con_target_user, con_target_passwd, table_name, con_target_db_name, \
                  time_word, get_syn_time, count_int, poolcount, pagesize]
        parmas[len(parmas) - 1] = pagesize
        loging("异常执行：" + str(parmas))
        pool = ThreadPoolExecutor(1)
        pool.submit(task, parmas)
        execpt_starting = "线程" + str(pagesize) + "：异常信息: " + str(e) + "starting"
        loging(execpt_starting.center(100, "--"))
        pool.shutdown(wait=True)
        execpt_end = "线程" + str(pagesize) + "：异常信息: " + str(e) + "end"
        loging(execpt_end.center(100, "--"))
        except_fun(traceback,execpt_start,execpt_starting,execpt_end)

    finally:
        if conn_target.open:
            conn_target.close()

        if conn_source.open:
            conn_source.close()


def data_syn_thread():
    try:
        file_path = file_system_path() + "/tools/tables_config/data_syn_test.xlsx"
        lineCount = OperaExcel.get_lines(file_path)
        OperaExcel.clean_up(file_path, "R2", "R" + str(lineCount))
        for line in range(lineCount - 1):
            line += 1
            colmun_count = OperaExcel.get_colmun(file_path)
            colmun_lists = []
            for colmun in range(colmun_count):
                colmun_lists.append(OperaExcel.get_cell(file_path, line, colmun))

            count_int, thread_count, con_source_host, con_source_port, con_source_user, con_source_passwd, \
            con_source_db_name, con_source_table_name, con_source_count, con_target_host, con_target_port, \
            con_target_user, con_target_passwd, con_target_db_name, table_name, con_target_count, status, \
            syn_point, time_word, get_syn_time = colmun_lists

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

                cursor_source.execute(
                    "select count(*) from " + table_name + " where " + time_word + " >= '" + str(get_syn_time) + "'")
                source_count = cursor_source.fetchall()
                count_jl = list(source_count[0].values())[0]
                cursor_source.execute("select count(*) from " + table_name)
                count_jl_source = cursor_source.fetchall()
                count_jl_source = list(count_jl_source[0].values())[0]
                OperaExcel.save_data_count(line + 1, colmun_lists.index(con_source_count) + 1, count_jl_source,
                                           file_path)
                poolcount = math.ceil(count_jl / count_int)
                parmas = [con_source_host, con_source_port, con_source_user, con_source_passwd, con_source_db_name,
                          con_target_host, con_target_port, con_target_user, con_target_passwd, table_name,
                          con_target_db_name, time_word,
                          get_syn_time, count_int, poolcount, 0]
                # 如果总记录数大于10000
                if count_jl >= count_int:
                    # 总记录数除以10000等于虚拟线程数

                    tcp_str = "数据库：【" + con_target_db_name + "】,表名：【" + table_name + "】,总记录数：【" + str(
                        count_jl) + "】,线程数总数：【" + str(poolcount) + "】,开启最大线程数：【" + str(thread_count) + "】"
                    loging(tcp_str.center(100, "*"))

                    # 虚拟线程总数
                    p_count = math.ceil(poolcount / thread_count)
                    # 计数器
                    sum = 0
                    # 虚拟线程数大循环
                    for iny in range(p_count):
                        # 线程数循环
                        pool = ThreadPoolExecutor(thread_count)
                        for inx in range(thread_count):
                            sum = sum + 1
                            parmas[len(parmas) - 1] = sum
                            pool.submit(task, parmas)  # 异步提交任务，提交后不用管进程是否执行
                        pool.shutdown(wait=True)



                else:
                    parmas[len(parmas) - 1] = 1
                    task(parmas)

                cursor_target.execute("select count(*) from " + table_name)
                count_jl_target = cursor_target.fetchall()
                count_jl_target = list(count_jl_target[0].values())[0]
                OperaExcel.save_data_count(line + 1, colmun_lists.index(con_target_count) + 1, count_jl_target,
                                           file_path)
                conn_close(conn_target, conn_source)

            OperaExcel.save_run_result(line + 1, colmun_lists.index(syn_point) + 1, file_path)
            OperaExcel.save_data_syn(line + 1, colmun_lists.index(get_syn_time) + 1, file_path)
            k_end = "数据库:【" + con_target_db_name + "】 表:【" + table_name + "】同步完成"
            loging(k_end.center(100, "*"))



        else:
            k_t = "无需同步数据库:【" + con_target_db_name + "】 表:【" + table_name + "】数据"
            loging("".center(100, "*"))
            loging(k_t.center(100, "*"))
            loging("".center(100, "*"))
            loging("")

    except Exception as e:
        except_fun(traceback)
        loging("data_syn_thread:异常信息: " + str(e))



    finally:
        if conn_target.open:
            conn_target.close()

        if conn_source.open:
            conn_source.close()


def conn_close(conn_target, conn_source):
    conn_target.close()
    conn_source.close()


if __name__ == '__main__':
    start = now_timestamp()
    data_syn_thread()
    time_cl = now_timestamp() - start
    loging("同步执行完成：总计耗时" + str(time_cl / 60) + "分")
    loging("同步执行完成：总计耗时" + str(time_cl) + "秒")
