from ..db import db_execute


# Get user info with the input account_id
def get_user_info(account_id):
    sql = "SELECT AccountId, UserName, NickName, Administrator, AvatarSuffix FROM users WHERE AccountId = {};"
    return db_execute(sql.format(account_id))


# Get all file info belonging to the user with the input account_id
def get_user_files(account_id):
    sql = "SELECT * FROM files WHERE AccountId = {} ORDER BY LastModified DESC;"
    return db_execute(sql.format(account_id))


# Add new file with the given account_id, file name, file type, and current time
# If file already exist for the given user, updatlast_modified
def add_new_file(account_id, file_name, file_type, last_modified):
    sql = "SELECT FileId FROM files WHERE AccountId = {} AND FileName = '{}';"
    same_name_file_num = len(db_execute(sql.format(account_id, file_name)))

    if same_name_file_num != 0:
        sql = "UPDATE files SET LastModified = '{}' WHERE AccountId = {} AND FileName = '{}';"
        db_execute(sql.format(last_modified, account_id, file_name))
    else:
        sql = "INSERT INTO files(AccountId, FileName, FileType, LastModified) VALUES ({}, '{}', {}, '{}');"
        db_execute(sql.format(account_id, file_name, file_type, last_modified))


# Check belonging of the specific file with the given account_id and file_id, return the file name
def check_belonging(account_id, file_id):
    sql = "SELECT FileName FROM files WHERE FileId = {} AND AccountId = {};"
    return db_execute(sql.format(file_id, account_id))


# Delete file with the given file id
def delete_file(file_id):
    sql = "DELETE FROM files WHERE FileId = {};"
    db_execute(sql.format(file_id))
