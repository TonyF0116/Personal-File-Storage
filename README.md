# Personal-File-Storage

A personal file storage system, in which you can store and view pictures and other files. You can also create and edit simple excel and pdf files. 

The website implements SSO (Single Sign On) using JWT. Token was stored in Authorization header and cookies. Some modification was made to enable the using of header authorization in swagger and to simulate the SSO process on different websites (now happening on account page, index page, and edit page).

flasgger is used for api demonstration. Visit http://127.0.0.1:5000/apidocs/ when the app is running for more info.

Run with the following steps:

1. Run `pip install -r requirements.txt && npm install`
2. Modify configurations in personal_file_storage/config.py
3. Make sure the terminal is at the root folder for this repo, which contains this 'README.md' (otherwise, file uploading and storing might be affected)
4. Run app.py (`python app.py`)