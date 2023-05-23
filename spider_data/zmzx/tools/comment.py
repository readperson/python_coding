import sys

sys.path.append("/opt/data_captureAPP")
from zmzx.tools.json_package import json_package
from tools.handl_specialcharacters import hzs_sub
from tools.base64_text import text_conversion_base64


def comment(comments, id_name, ids):
    comment_dict = {}
    comment_dict[id_name] = ids
    json_package(comments, "id", "", comment_dict)
    json_package(comments, "sender_id", "", comment_dict)
    json_package(comments, "sender_nick_name", "", comment_dict)
    comment_dict["sender_nick_name"] = hzs_sub(comment_dict["sender_nick_name"])
    json_package(comments, "sender_photo_url", "", comment_dict)
    json_package(comments, "content", "", comment_dict)
    comment_dict["content"] = text_conversion_base64(comment_dict["content"])
    json_package(comments, "send_time", "", comment_dict)
    return comment_dict
