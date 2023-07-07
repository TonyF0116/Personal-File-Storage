from ..db import db_execute


# Get user info with the input account_id
def get_user_info(account_id):
    sql = "SELECT AccountId, UserName, NickName, Administrator, AvatarSuffix FROM users WHERE AccountId = {}"
    return db_execute(sql.format(account_id))


# Get all file info belonging to the user with the input account_id
def get_user_files(account_id):
    sql = "SELECT * FROM files WHERE AccountId = {}"
    return db_execute(sql.format(account_id))


# Add new file with the given account_id, file name, file type, and current time
def add_new_file(account_id, file_name, file_type, last_modified):
    sql = "INSERT INTO files(AccountId, FileName, FileType, LastModified) VALUES ({}, '{}', {}, '{}')"
    db_execute(sql.format(account_id, file_name, file_type, last_modified))
