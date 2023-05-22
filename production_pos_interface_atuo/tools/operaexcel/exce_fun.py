import sys
from tools.file_system_path import file_system_path

sys.path.append(file_system_path())


def code_read():
    environment_path = file_system_path() + "/tools/operaexcel/code_config.txt"
    with open(environment_path, "r", encoding="utf-8") as f:
        return f.read()


def excel_templet():
    environment_path = file_system_path() + "/tools/operaexcel/excel_templet.txt"
    with open(environment_path, "r", encoding="utf-8") as f:
        title = f.read().split(",")
        return title


if __name__ == '__main__':
    excel_templet()
