from tools.get_time import get_now_time_y_m_d
from tools.get_time import file_system_path
import os
from tools.get_time import get_now_time
from tools.logconfig.logingconfig import loging


def except_fun(traceback,execpt_start,execpt_starting,execpt_end):
    path = file_system_path() + "/tools/logs/" + get_now_time_y_m_d() + "/except_logs"
    isExists = os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
    tra = str(traceback.format_exc())
    str_except = '未知错误异常：' + tra
    loging(str_except)
    with open(path + "/" + get_now_time_y_m_d() + ".txt", "a+") as f:
        f.write(str(get_now_time()) + " " + str_except)
        f.write("\r\n")
        f.write(str(get_now_time()) + " " + execpt_start)
        f.write("\r\n")
        f.write(str(get_now_time()) + " " + execpt_starting)
        f.write("\r\n")
        f.write(str(get_now_time()) + " " + execpt_end)
        f.write("\r\n")
