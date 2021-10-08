import pymysql.cursors

con = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'updownloadfile',
            cursorclass = pymysql.cursors.DictCursor
            )