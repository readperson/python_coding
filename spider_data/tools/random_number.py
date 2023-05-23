import random

'''
随机点赞数
'''


def random_number_likes():
    return str(random.randint(100, 2000))


def random_number():
    return str(random.randint(50, 500))


'''
随机阅读数
'''


def random_number_readings():
    return str(random.randint(100, 2000))


'''
红单随机价格
'''


def random_number_price_red_list():
    return str(random.randint(400, 500))


def random_number_price():
    return str(random.randint(10, 50))


def random_number_status():
    return str(random.randint(10, 50))


"""
随机背景颜色
"""


def random_color_list():
    color = ["#7ab566", "#666666", "#74a0de", "#055896", "#ffa000", "#5c82ff"]
    color_int = random.randint(0, int(len(color)) - 1)
    return color[color_int]


"""
社区圈子随机
"""


def random_circle_list():
    circle = ["天下足球圈", "中国篮球圈", "NBA赛场圈", "篮网圈"]
    circle_int = random.randint(0, int(len(circle)) - 1)
    return circle[circle_int]


"""
随机beginTime
"""


def random_beginTime():
    return str(random.randint(10, 23)) + ":" + str(random.randint(10, 59))


'''
随机城市
'''


def random_city():
    city_list = ["广州市", "深圳市", "北京市", "上海市", "铁岭市", "营口市", "青岛市", "枣庄市", "福州市", "西安市"]
    city_index = random.randint(0, 9)
    city = city_list[city_index]
    return city


"""
随机年
"""


def random_year():
    return random.randint(2, 10)
