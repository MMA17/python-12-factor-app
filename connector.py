import pymysql.cursors
import os
con = pymysql.connect(
            host = os.getenv('MYSQL_HOST'),
            user = os.getenv('MYSQL_USER'),
            password = os.getenv('MYSQL_PASS'),
            database = os.getenv('MYSQL_DATABASE'),
            cursorclass = pymysql.cursors.DictCursor
            )
