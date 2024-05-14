import pymysql

mysql = None


def init_db(config):
    global mysql
    host, user, password, db = [config[_] for _ in ['HOST', 'USERNAME', 'PASSWORD', 'DB_NAME']]
    mysql = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        cursorclass=pymysql.cursors.DictCursor
    )


def get_db():
    return mysql
