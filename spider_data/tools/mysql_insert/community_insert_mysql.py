import pymysql
import datetime


def commit_mysqlDB(contentId, title, nickName, hitsCount, pubTime, srcName, contentTxt, littleImg, channelIconPath,
                   headImageUrl,icon_image, communities_json):
    try:
        db = pymysql.connect("47.97.79.60", "root", "#2020mysql56root", "tyds", charset='utf8')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql_query = "SELECT * FROM communities  WHERE contentId='%s' " % (contentId)
        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime(
            "%Y-%m-%d %H:%M:%S")
        cursor.execute(sql_query)
        data_query = cursor.rowcount
        if data_query == 0:
            id_query = "SELECT MAX(id) FROM communities "
            num = cursor.execute(id_query)
            if num > 0:
                num1 = cursor.fetchall()
                ids = num1[0]
                id = ids[0]
                if id == None:
                    id = 1
                else:
                    id = id + 1

            print("-------------社区ID" + contentId + "插入成功：时间" + capture_time + "-----------------")
            # # SQL 插入语句
            sql_insert = "INSERT INTO communities (contentId,title,nickName, hitsCount, pubTime, srcName," \
                         "contentTxt,littleImg,id,channelIconPath,HeadImgUrl,icon_image)" \
                         "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%d','%s','%s','%s')" \
                         % (
                             contentId, title, nickName, hitsCount, pubTime, srcName, contentTxt,
                             littleImg, id, channelIconPath, headImageUrl,icon_image)

            # 执行sql语句
            cursor.execute(sql_insert)
            print("-------------评论" + contentId + "-----------------")
            # SQL 插入语句
            sql_insert = "INSERT INTO comment(contentId,communities_json) VALUES ('%s','%s')" % (
                contentId, communities_json)
            # 执行sql语句
            cursor.execute(sql_insert)
            # 提交到数据库执行
            db.commit()


        else:
            print(contentId, "社区已存在,不能插入数据-------")
    except Exception as e:
        print(
            "————————————————————————————插入数据异常,事物已回滚" + capture_time + "————————————————————————————————————")
        db.rollback()
        print(e)


print("")
