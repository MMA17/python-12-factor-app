import pymysql.cursors

con = pymysql.connect(
            host = 'mysql',
            user = 'root',
            password = '123456',
            database = 'updownloadfile',
            cursorclass = pymysql.cursors.DictCursor
            )