# import mysql.connector
# from mysql.connector import connection

# mydb = mysql.connector.connect(
#     host = 'localhost',
#     user = 'root',
#     password = '',
#     database = "updownloadfile"
# )

# print(mydb)
# mydb.close()

import pymysql.cursors

con = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'updownloadfile',
    cursorclass = pymysql.cursors.DictCursor
)

with con:
    with con.cursor() as cursor:
        # Create a new record
        sql = "SELECT * FROM users WHERE username = %s AND pass = %s"
        cursor.execute(sql, ('hoangviet','passwd'))
        result = cursor.fetchall()
        print(result)
        for row in result:
            print(row["user_id"])
            print(row["username"])
            print(row["pass"])

#con.close()

