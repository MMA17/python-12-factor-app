import pymysql.cursors

con = pymysql.connect(
            host = '123.31.39.251',
            user = 'root',
            password = '123456',
            database = 'updownloadfile',
            cursorclass = pymysql.cursors.DictCursor
            )