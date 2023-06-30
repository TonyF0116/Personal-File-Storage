import pymysql
from .config import host, port, user, password, db


def db_execute(sql):
    with pymysql.connect(host=host, port=port, user=user, password=password, db=db) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
    return result
