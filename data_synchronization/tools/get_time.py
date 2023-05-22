import sys
from tools.file_system_path import file_system_path

sys.path.append(file_system_path())
import datetime
import time


def get_now_time():
    '''
    返回当前系统时间
    格式:%Y-%m-%d %H:%M:%S
    :return:
    '''
    return (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")


def get_now_time_underline():
    '''
    返回当前时间 没有空格
    格式:%Y-%m-%d_%H_%M_%S
    :return:
    '''
    return (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d_%H_%M_%S")


def get_now_time_y_m_d():
    '''
    返回当前时间 年月日
    格式:%Y-%m-%d
    :return:
    '''
    return (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d")


def get_now_time_h():
    '''
    返回年月日时
    :return:
    '''
    return (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d_%H")


def get_time_revert(t_ime):
    '''
    返回当前时间的前后分钟数
    datetime.datetime.now() + datetime.timedelta(minutes=t_ime)).strftime("%Y-%m-%d %H:%M:%S"
    :param t_ime:
    :return:
    '''
    return (datetime.datetime.now() + datetime.timedelta(minutes=t_ime)).strftime("%Y-%m-%d %H:%M:%S")


def timestamp_conversion_date(timestamp):
    '''
    将时间戳转换为年月日 时分秒
    格式：%Y-%m-%d %H:%M:%S
    :param timestamp:
    :return:
    '''
    timestamp = time.localtime(int(timestamp))
    return time.strftime("%Y-%m-%d %H:%M:%S", timestamp)


def now_timestamp():
    '''
    返回当前时间戳
    :return:
    '''
    return int(time.time())


if __name__ == '__main__':
    print(get_now_time_h())
