DROP TABLE IF EXISTS users;
CREATE TABLE users 
(
AccountId INT AUTO_INCREMENT, 
UserName VARCHAR(50),
NickName VARCHAR(50),
Password VARCHAR(64),           # stores SHA256 of the password
Administrator INT,              # 0 is normal user, 1 is administrator
AvatarSuffix VARCHAR(10),
PRIMARY KEY (AccountId)
);

DROP TABLE IF EXISTS files;
CREATE TABLE files 
(
FileId INT AUTO_INCREMENT, 
AccountId INT,                  # Belonging
FileName VARCHAR(128), 
FileType INT,                   # 0 is pic, 1 is pdf, 2 is excel
LastModified DATETIME,
PRIMARY KEY (FileId),
FOREIGN KEY (AccountId) REFERENCES users(AccountId)
);