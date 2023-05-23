import base64

'''
对文本内容进行base64处理
'''


def text_conversion_base64(content):
    base64_content = base64.b64encode(content.encode('utf-8'))
    return (str(base64_content, 'utf-8'))


"""
base64 转化为文本
"""


def base64_conversion_text(content):
    base64_content = base64.b64decode(content.encode('utf-8'))
    return (str(base64_content, 'utf-8'))
