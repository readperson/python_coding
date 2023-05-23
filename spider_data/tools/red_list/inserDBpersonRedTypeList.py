import datetime
import pymysql


def inserDBpersonRedTypeList(uid, name, red_type, reuslt):
    try:
        db = pymysql.connect("47.97.79.60", "root", "#2020mysql56root", "tyds", charset='utf8')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql_query = "SELECT * FROM red_person_redtypelist  WHERE uid='%s'and type='%s' " % (uid, red_type)
        capture_time = (datetime.datetime.now() + datetime.timedelta()).strftime(
            "%Y-%m-%d %H:%M:%S")
        cursor.execute(sql_query)
        data_query = cursor.rowcount
        if data_query == 0:
            id_query = "SELECT MAX(id) FROM red_person_redtypelist "
            num = cursor.execute(id_query)
            if num > 0:
                num1 = cursor.fetchall()
                ids = num1[0]
                id = ids[0]
                if id == None:
                    id = 1
                else:
                    id = id + 1

            print("-------------人员ID" + uid + "插入成功：时间" + capture_time + "-----------------")
            # # SQL 插入语句
            sql_insert = "INSERT INTO red_person_redtypelist (id,uid,name,type,red_type_list)" \
                         "VALUES ('%s','%s','%s','%s','%s')" \
                         % (
                             id, uid, name, red_type, reuslt)
            cursor.execute(sql_insert)
            db.commit()


        else:
            print(uid, red_type, "红单数据已存在,不能插入数据-------")
    except Exception as e:
        print(
            "————————————————————————————插入数据异常,事物已回滚" + capture_time + "————————————————————————————————————")
        db.rollback()
        print(e)


print("")
