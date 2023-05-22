import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.environment_config.environment_config import environment_config
from tools.project_name.project_name import pname_r_f


def case_path():
    '''
        获取测试用例路径
        :return: 测试用例路径
        '''
    pname = pname_r_f()
    if environment_config() == "Y":
        return "/var/jenkins_home/workspace/pull_order_interface_auto_case/order_file_case/case_file/" + pname + "/" + pname + ".xlsx"
    else:
        fname = "D:\pythonworkspace\order_interface_auto_case\order_file_case\case_file\\" + pname + "\\" + pname + ".xlsx"
        return fname
