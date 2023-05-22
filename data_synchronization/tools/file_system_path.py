import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def file_system_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
