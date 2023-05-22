import sys
from tools.file_system_path import file_system_path

sys.path.append(file_system_path())
import logging
from tools.get_time import get_now_time
from tools.get_time import get_now_time_y_m_d
import os


def loging(logs):
    '''日志处理'''
    # 保存文件

    path = file_system_path() + "/tools/logs/" + get_now_time_y_m_d()
    isExists = os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
    file = open(path + "/" + get_now_time_y_m_d() + '.txt', encoding="utf-8", mode="a")
    logging.basicConfig(stream=file, format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO,
                        filemode="a")

    logging.info(logs)
    print(get_now_time() + " INFO:", logs)


if __name__ == '__main__':
    loging("-----0000))))")
