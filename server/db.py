import pymysql
from .config import mysql_host, mysql_port, mysql_user, mysql_password, mysql_db


def db_execute(sql):
    with pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password, db=mysql_db) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
    return result
