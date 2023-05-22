import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.file_system_path import file_system_path
import requests
import json
from tools.logconfig.logingconfig import loging
from tools.dingding_send_messge.exception_msg_handle import exception_msg_handle
from tools.dingding_send_messge.zkj_dingSendMessage import zkj_dingSendMessage
from tools.dingding_send_messge.dingSendMessage import dingSendMessage
from tools.operaexcel.operaExcel import OperaExcel
from tools.get_time import get_now_time
from tools.environment_config.environment_config import environment_config
from tools.exception_info.exception_info import set_exception_info


def request_post(data, method, params, url):
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    result = json.loads(
        requests.post(url=url, data=data, headers=header).text.replace('"null"', '""').replace("null", '""'))
    loging("sql_name: " + str(result.get("sql_name")))
    loging("url: " + str(url))
    loging("method: " + str(method))
    loging("header: " + str(header))
    loging("data: " + str(data))
    loging("result: " + str(result))
    loging("")
    parameters = {"url": url, "header": header, "data": data, "params": params, "result": result, "method": method}
    request_result_write(**parameters)

    return result


def request_post_login(url, data, method, params):
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    result = json.loads(requests.post(url=url, data=data, headers=header).text.replace("null", '""'))
    loging("url: " + str(url))
    loging("method: " + str(method))
    loging("header: " + str(header))
    loging("data: " + str(data))
    loging("result: " + str(result))
    parameters = {"url": url, "header": header, "data": data, "params": params, "result": result}
    request_result_write(**parameters)
    return result


def request_result_write(**parameters):
    file_path = OperaExcel.create_excel()
    result = parameters['result']
    if isinstance(result, dict):
        if "message" in result:
            with open(file_system_path() + "/tools/fail_keyword/fail_keyword.txt", "r", encoding="utf-8") as f:
                keyword_str = f.readline().split(",")
                for keyword in keyword_str:
                    if result["message"].find(keyword) != -1:
                        set_exception_info("Exception")
                        # 出现异常发送钉钉消息
                        msg = exception_msg_handle(parameters.get("url"), parameters.get("params"),
                                                   parameters.get("method"), parameters.get("header"),
                                                   parameters.get("data"), result)
                        if environment_config() == "Y":
                            loging("look! look! look! interface exception send 钉钉 ERROR......")
                            loging("look! look! look! interface exception send 钉钉 ERROR......")
                            zkj_dingSendMessage(msg)
                        loging("look! look! look! interface exception send 钉钉 ERROR......")
                        dingSendMessage(msg)

        # else:
        #     loging("返回结果无message!")
        lines = OperaExcel.get_lines(file_path)
        status = "Fail"
        for value in result.values():
            if str(value).find("成功") != -1:
                status = "Success"
                break

        OperaExcel.request_result_new(lines + 1, get_now_time(), str(parameters.get("url")),
                                      str(parameters.get("params")), str(parameters.get("method")),
                                      str(parameters.get("header")), str(parameters.get("data")),
                                      str(result), status, file_path)

    elif isinstance(result, str):
        lines = OperaExcel.get_lines(file_path)
        OperaExcel.request_result_new(lines + 1, get_now_time(), str(parameters.get("url")),
                                      str(parameters.get("params")), str(parameters.get("method")),
                                      str(parameters.get("header")), str(parameters.get("data")),
                                      str(result), "Success", file_path)
