from ..db import db_execute


# Get file info with the given file id
def get_file_info(file_id):
    sql = "SELECT AccountId, FileName, FileType FROM files WHERE FileId = {}"
    return db_execute(sql.format(file_id))
