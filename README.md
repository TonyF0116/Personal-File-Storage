# Personal-File-Storage

A personal file storage system, in which you can store and view pictures and other files. You can also create and edit simple excel and pdf files. 

The website implements SSO (Single Sign On) using JWT. Token was stored in Authorization header. Some modification was made to simulate the SSO process on different websites (now happening on account page, index page, and edit page).

flasgger is used for api demonstration. Visit http://127.0.0.1:5000/apidocs/ when the app is running for more info.

Run with the following steps:

1. Run pip install -r requirements.txt
2. Modify database configurations in personal_file_storage/config.py
3. Make sure the terminal is at the root folder for this repo, which contains this 'README.md' (otherwise, file uploading and storing might be affected)
4. Run app.py

To implement:
1. ~~Account Page~~
2. ~~JWT~~
3. Index Page
4. Pic
5. Edit Page(PDF/Excel) /Email
6. Swagger
7. Redis（excel templates）/Log
