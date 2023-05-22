import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pos_handle.login.login import timestamp_login
from tools.case_path import case_path
from tools.operaexcel.operaExcel import OperaExcel
from tools.get_time import get_now_time
from tools.logconfig.logingconfig import loging
from tools.git_file_upload.git_file_upload import git_file_upload
from tools.exception_info.exception_info import get_exception_info
from tools.exception_info.exception_info import set_exception_info
from tools.url_cahe.url_cahe import set_url
from tools.goods import set_goods
from pos_handle.pos_01gmth.gmth import goumai_tuihuo
from pos_handle.logout.logout import logout
from pos_handle.pos_01gmth.gmth_01gmth.gmth_handle.jiaoban.handover import handover
import traceback


def run():
    case_file = case_path()
    lines_count = OperaExcel.get_lines(case_file)
    colmuns_count = OperaExcel.get_colmun(case_file)
    OperaExcel.clean_up(case_file, "B2", "B" + str(lines_count))
    Success_count = 0
    Fail_count = 0
    ignore_count = 0
    run_dict = {}

    try:
        for line in range(lines_count - 1):
            line += 1
            case_files_list = []
            for colmun in range(colmuns_count):
                case_files_list.append(OperaExcel.get_cell(case_file, line, colmun))

            status, run_position, run_time, url, loginname, password, testing_name, goods, login_interval, module_name, run_method, results = case_files_list
            if status == "Y":
                set_goods(goods)
                timestamp_login(loginname, password, url, login_interval, testing_name)
                set_url(url)
                start = " Strating.....【" + module_name + "】功能接口测试 "
                loging(start.center(50, "*"))

                exec(run_method + "()")

                if get_exception_info() == "None":
                    run_dict[module_name] = "Success"
                    Success_count += 1
                    OperaExcel.save_run_result(line + 1, 12, "Success", False, case_file)
                if get_exception_info() == "Exception":
                    Fail_count += 1
                    run_dict[module_name] = "Fail"
                    OperaExcel.save_run_result(line + 1, 12, "Fail：[有接口异常，查看excle日志记录和钉钉消息]", True, case_file)
                set_exception_info("None")
                OperaExcel.save_run_result(line + 1, 2, "Y", False, case_file)
                OperaExcel.save_run_result(line + 1, 3, str(get_now_time()), False, case_file)
                end = " End ..... 【" + module_name + "】功能接口测试 "
                loging(end.center(50, "*"))
                loging("")
                handover()
                logout()

            else:
                start = " ignore.....【" + module_name + "】功能接口测试 "
                OperaExcel.save_run_result(line + 1, 12, "ignore", False, case_file)
                ignore_count += 1
                run_dict[module_name] = "ignore"
                loging(start.center(50, "*"))

        loging(
            "总计：" + str(lines_count - 1) + "个功能模块,成功" + str(Success_count) + "个，失败：" + str(
                Fail_count) + "个,ignore：" + str(
                ignore_count) + "个")
        loging(run_dict)
        git_file_upload()

    except Exception as e:
        handover()
        logout()
        git_file_upload()
        loging("异常INFO: " + str(e))
        loging('未知错误异常：' + str(traceback.format_exc()))




if __name__ == '__main__':
    run()
