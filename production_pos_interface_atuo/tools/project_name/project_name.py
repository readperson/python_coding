import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.file_system_path import file_system_path


def project_name():
    file_paths = file_system_path().replace("\\", "A_^").replace("/", "A_^").split("A_^")
    return file_paths[int(len(file_paths)) - 1]


def pname_r_f():
    pname = file_system_path() + "/tools/project_name/projet_name.txt"
    with open(pname, "r", encoding="utf-8")as f:
        return f.read()


if __name__ == '__main__':
    print(pname_r_f())
