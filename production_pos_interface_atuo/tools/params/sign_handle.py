import sys

from tools.file_system_path import file_system_path

sys.path.append(file_system_path())
from hashlib import sha1
from tools.logconfig.logingconfig import loging


def sign_handle(salt, method, params, ctx_id, timestamp):
    '''
    签名方法 规则： salt, method, params, ctx_id, timestamp
    Sign=sha1(salt+排序（method,params,ctx_id,timestamp的键名及值）+ salt）
    :param salt:
    :param method:
    :param params:
    :param ctx_id:
    :param timestamp:
    :return:sign
    '''
    sign = salt + "method" + method + "params" + params + "ctx_id" + ctx_id + "timestamp" + timestamp + salt
    s1 = sha1()  # 创建sha1加密对象
    s1.update(sign.encode("utf-8"))  # 转码（字节流）
    sign = s1.hexdigest()
    loging("sign：" + str(sign))
    return sign  # 将字节码转成16进制
