import sys
from tools.file_system_path import file_system_path

sys.path.append(file_system_path())


def data_handle(method, sign, params, timestamp, ctx_id):
    '''
    :param method:
    :param sign:
    :param params:
    :param timestamp:
    :param ctx_id:
    :return: "method=" + method + "&sign=" + sign + "&params=" + params + "&timestamp=" + timestamp + "&ctx_id=" + ctx_id
    '''

    # method=gb.cexport.data.export&params=&app_key=12000&timestamp=20210824152927&data_sign=0
    # &ids=12&ctx_id=f7f42c097684401a8bb51ba666edcac3&sign=f21818b7987677ab8e45c6c0326e8da2911be026
    # return "method=" + method + "&sign=" + sign + "&params=" + params + "&timestamp=" + timestamp + "&ctx_id=" + ctx_id + "&app_key=" + str(
    #     12000) + "&ids=" + str(12) + "&data_sign=" + str(0)
    return "method=" + method + "&sign=" + sign + "&params=" + params + "&timestamp=" + timestamp + "&ctx_id=" + ctx_id
