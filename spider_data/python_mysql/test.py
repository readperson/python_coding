import pymysql
import base64

s ="123456"
s1 = base64.b64encode(s.encode('utf-8'))
t1 = (str(s1, 'utf-8'))
print(t1)
# db = pymysql.connect("47.97.79.60", "root", "#2020mysql56root", "tyds", charset='utf8')
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()
# sql_query = "SELECT * FROM comment  WHERE contentId='%s'" % (
#     "49723dd1-a1bb-4cf0-ae35-113190e10396")
# cursor.execute(sql_query)
# data_query = cursor.rowcount
# print("sql_query---:%s" % sql_query)
# print(type(data_query))
# # print(len(data_query))
# print("data_query---:",data_query)