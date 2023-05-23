import datetime
import time

"""
返回当前时间
"""


def now_time():
    return (datetime.datetime.now() + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")


"""
返回几分钟前的时间
"""


def now_time_revert(t_ime):
    return (datetime.datetime.now() + datetime.timedelta(minutes=-t_ime)).strftime("%Y-%m-%d %H:%M:%S")


"""
将时间戳转换为年月日 时分秒
"""


def timestamp_conversion_date(timestamp):
    timestamp = time.localtime(int(timestamp))
    return time.strftime("%Y-%m-%d %H:%M:%S", timestamp)


"""
返回当前时间戳
"""


def now_timestamp():
    return int(time.time())
