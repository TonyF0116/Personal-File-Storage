from ..db import db_execute


# Get user info with the input account_id
def get_user_info(account_id):
    sql = "SELECT * FROM users WHERE AccountId = {}"
    return db_execute(sql.format(account_id))


# Get all file info belonging to the user with the input account_id
def get_user_files(account_id):
    sql = "SELECT * FROM files WHERE AccountId = {}"
    return db_execute(sql.format(account_id))
