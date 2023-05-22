import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def environment_config():
    environment_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))) + "/environment_config/environment_config.txt"
    with open(environment_path, "r", encoding="utf-8") as f:
        return f.read()