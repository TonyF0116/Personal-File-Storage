from ..db import db_execute


# Get file info with the given file id
def get_file_info(file_id):
    sql = "SELECT AccountId, FileName, FileType FROM files WHERE FileId = {}"
    return db_execute(sql.format(file_id))


# Update file last_modified for the given file_id
def update_file_modify_time(file_id, last_modified):
    sql = "UPDATE files SET LastModified = '{}' WHERE FileId = {};"
    db_execute(sql.format(last_modified, file_id))
