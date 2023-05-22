from tools.login_cache.login_cache import get_login_domian_token


def json_header():
    headers = {
        'Host': 'portal.testting.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Authorization': get_login_domian_token().get("token")
        # 'Referer': 'http://portal.testting.com/backend/perm/index.html'
    }

    return headers


def from_post_header():
    headers = {
        'Host': 'portal.testting.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Authorization': get_login_domian_token().get("token"),
    }

    return headers


def sesssion_header():
    header = {
        "Host": "report.testting.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": "Bearer " + get_login_domian_token().get("token"),
        "sessionID": "c59b8e03-689c-42d9-93df-1405d74f8d4d"
    }
    return header
