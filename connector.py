import pymysql.cursors

con = pymysql.connect(
            host = '10.93.241.2',
            user = 'root',
            password = '123456',
            database = 'updownloadfile',
            cursorclass = pymysql.cursors.DictCursor
            )