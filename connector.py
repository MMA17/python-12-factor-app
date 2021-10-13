import pymysql.cursors

con = pymysql.connect(
            host = '103.56.156.1999',
            user = 'root',
            password = '123456',
            database = 'updownloadfile',
            cursorclass = pymysql.cursors.DictCursor
            )
