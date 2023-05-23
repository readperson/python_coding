import re

"""
去除特殊字符，只保留汉子，字母、数字
sub(pattern,repl,string) 	把字符串中的所有匹配表达式pattern中的地方替换成repl
[^**] 	表示不匹配此字符集中的任何一个字符
\u4e00-\u9fa5 	汉字的unicode范围
\u0030-\u0039 	数字的unicode范围
\u0041-\u005a 	大写字母unicode范围
\u0061-\u007a 	小写字母unicode范围
\uAC00-\uD7AF 	韩文的unicode范围
\u3040-\u31FF 	日文的unicode范围
"""


def hzs_sub(string):
    return re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", string)

def chinese_character(string):
    return re.sub(u"([^\u4e00-\u9fa5])", "", string)


