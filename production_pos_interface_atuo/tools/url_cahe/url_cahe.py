dict_url = {}


def set_url(url):
    dict_url["url"] = url


def get_url():
    return dict_url.get("url")
