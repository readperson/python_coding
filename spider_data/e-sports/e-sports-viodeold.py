from tools.time_treatment import *
import requests
import json

# 视频可用
def e_sports_viode():
    url = "https://api.lewandj.com/gateway/content-service/app/v1/index/content/recommend-list?categoryId=4&pageNum=6&pageSize=10"
    headers = {
        "timestamp": str(now_timestamp()) + "456",
        "appId": "10001",
        "nonce": "jKBBjjof1BzXRdy3LcB0vWpcYdQ51mDx",
        "appVersion": "2.3.1",
        "channel": "android-huawei",
        "deviceCode": "2d6d64df-f4f2-4f61-9de2-28e915b36b27",
        "sign": "6c3d66a6a9aaa2f5ffc79375677850ae",
        "Host": "api.lewandj.com"
    }
    reps = requests.get(url=url, headers=headers).text
    reps = json.loads(reps)
    print(reps)
    reps_count = int(len(reps["data"]))
    i = 1
    for r_count in range(reps_count):
        base = {}
        title = reps["data"][r_count]["title"]
        print(title)
        cuid = reps["data"][r_count]["cuid"]
        nickname = reps["data"][r_count]["nickname"]
        avatar = reps["data"][r_count]["avatar"]
        videoUrl = reps["data"][r_count]["videoUrl"]
        imgUrls = reps["data"][r_count]["imgUrls"]
        enjoy = reps["data"][r_count]["enjoy"]
        comment = reps["data"][r_count]["comment"]
        gameDesc = reps["data"][r_count]["gameDesc"]
        circleName = reps["data"][r_count]["circleName"]
        createAt = reps["data"][r_count]["createAt"]
        createAt = str(createAt)[0:10]
        createAt = timestamp_conversion_date(int(createAt))
        base["title"] = title
        base["cuid"] = cuid
        base["nickname"] = nickname
        base["avatar"] = avatar
        base["videoUrl"] = videoUrl
        base["imgUrls"] = imgUrls
        base["enjoy"] = enjoy
        base["comment"] = comment
        base["gameDesc"] = gameDesc
        base["circleName"] = circleName
        base["createAt"] = createAt

        comment_url = "https://api.lewandj.com/gateway/content-service/app/v1/comment/list?cuid=" + cuid + "&hotComment=1&uid=&pageNum=1&pageSize=10"
        # https://api.lewandj.com/gateway/content-service/app/v1/index/content/recommend-list?categoryId=4&pageNum=2&pageSize=10
        comment_headers = {
            "timestamp": str(now_timestamp()) + "456",
            "appId": "10001",
            "nonce": "JHCQdeU3Qgnal3LLOur2WvhZY1XPBPtS",
            "appVersion": "2.3.1",
            "channel": "android-huawei",
            "deviceCode": "2d6d64df-f4f2-4f61-9de2-28e915b36b27",
            "sign": "fef0ede61ca7cb0475fde94b400b8d97",
            "Host": "api.lewandj.com"
        }
        coment_reuslt = requests.get(url=comment_url, headers=comment_headers).text
        coment_reuslt = json.loads(coment_reuslt)
        comment_count = int(len(coment_reuslt["data"]))
        if comment_count > 0:
            print("  评论", comment_count)
        comment_list = []
        for c_count in range(comment_count):
            comment_dict = {}
            commentUid = coment_reuslt["data"][c_count]["commentUid"]
            comment = coment_reuslt["data"][c_count]["comment"]
            nickname = coment_reuslt["data"][c_count]["nickname"]
            avatar = coment_reuslt["data"][c_count]["avatar"]
            createAt = coment_reuslt["data"][c_count]["createAt"]
            createAt = str(createAt)[0:10]
            createAt = timestamp_conversion_date(createAt)
            comment_dict["commentUid"] = commentUid
            comment_dict["comment"] = comment
            comment_dict["nickname"] = nickname
            comment_dict["avatar"] = avatar
            comment_dict["createAt"] = createAt
            comment_list.append(comment_dict)
        base["comment_data"] = comment_list
        print("json:", str(base).replace("'", '"'))

        with open("./video/v" + str(i) + ".txt", "w", encoding="utf-8") as f:
            f.write(str(base).replace("'", '"'))
            i = i + 1


if __name__ == '__main__':
    e_sports_viode()
