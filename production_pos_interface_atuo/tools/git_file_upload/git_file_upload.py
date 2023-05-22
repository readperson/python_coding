import sys
from tools.file_system_path import file_system_path

sys.path.append(file_system_path())
from tools.file_system_path import file_system_path
from tools.environment_config.environment_config import environment_config
from tools.get_time import get_now_time_y_m_d
from tools.logconfig.logingconfig import loging
import os
from tools.project_name.project_name import project_name
from tools.project_name.project_name import pname_r_f


def git_file_upload():
    if environment_config() == "Y":
        pname = pname_r_f()
        now_time = get_now_time_y_m_d()
        loging("git: 正在push用例、日志文件.....")
        # 历史文件
        path_file = file_system_path() + "/case_data_file/" + str(
            project_name()) + "_" + get_now_time_y_m_d() + "_request_result.xlsx"
        # 用例文件
        case_file = "/var/jenkins_home/workspace/pull_order_interface_auto_case/order_file_case/case_file/" + pname + "/" + pname + ".xlsx"
        # log文件/var/jenkins_home/workspace/pull_oprytdion_pos_interface_atuo/tools/logs/2021-09-15/2021-09-15.txt
        #        /var/jenkins_home/workspace/pull_oprytdion_erp_client_interface_atuo/tools/logs/2021-09-09
        log_file = "/var/jenkins_home/workspace/pull_" + pname + "/tools/logs/" + now_time + "/" + now_time + ".txt"

        # 历史目标文件路径
        history_path_target = "/root/order_interface_auto_case/order_file_case/run_result/" + pname + "/history/"
        # 用例目标文件路径
        path_target = "/root/order_interface_auto_case/order_file_case/run_result/" + pname + "/"

        # log目标文件路径
        #                  /root/order_interface_auto_case/order_file_case/run_result/oprytdion_pos_interface_atuo/log/2021-09-15.txt
        log_path_target = "/root/order_interface_auto_case/order_file_case/run_result/" + pname + "/log/"

        # 处理历史文件
        with open(path_file, "rb") as f:
            img_stream = f.read()
            # 写入文件流
            file_paths = path_file.replace("\\", "A_^").replace("/", "A_^").split("A_^")
            # 切割目标文件
            file_history = file_paths[int(len(file_paths)) - 1]
            # 目标文件路径+切割目标文件 为复制文件路径
            target = history_path_target + file_history
            with open(target, "wb") as f1:
                f1.write(img_stream)

        # 处理用例文件
        with open(case_file, "rb") as f2:
            img_stream = f2.read()
            # 写入文件流
            file_case_paths = case_file.replace("\\", "A_^").replace("/", "A_^").split("A_^")
            # 切割目标文件
            file_case_history = file_case_paths[int(len(file_case_paths)) - 1]
            # 目标文件路径+切割目标文件 为复制文件路径
            target_case = path_target + file_case_history
            with open(target_case, "wb") as f3:
                f3.write(img_stream)

        # 处理log文件
        with open(log_file, "rb") as f4:
            img_stream = f4.read()
            # 写入文件流
            log_file_paths = log_file.replace("\\", "A_^").replace("/", "A_^").split("A_^")
            # 切割目标文件
            log_file_path = log_file_paths[int(len(log_file_paths)) - 1]
            # 目标文件路径+切割目标文件 为复制文件路径
            target_file = log_path_target + log_file_path
            with open(target_file, "wb") as f5:
                f5.write(img_stream)

        # 执行shell 脚本
        res_os = os.popen('/opt/run_git.sh')
        loging(res_os.read())
        loging("git: push用例、日志文件完成")
