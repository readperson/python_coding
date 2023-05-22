import sys
from tools.file_system_path import file_system_path

sys.path.append(file_system_path())
import base64
from tools.logconfig.logingconfig import loging
import json


def params_handle(params):
    params = json.dumps(params).replace("'", '"').replace('"true"', 'true').replace('"false"', 'false') \
        .replace('"null"', 'null').replace("\r", "").replace("\n", "").replace("\r\n", "")
    loging("params: " + params)
    params = base64.b64encode(bytes(params.encode("utf-8")))
    params = str(params, "utf-8").replace("b'", "").replace("'", "")
    return params


if __name__ == '__main__':
    params = {"sql_id": "GLOBAL-INFO-0001",
              "line_ai": "true",
              "input_param":
                  {"sub_unit_num_id": "100002"},
              "page_num": 1,
              "page_size": 10}
    params_handle(params)
