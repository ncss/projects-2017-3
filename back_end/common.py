import os
import hashlib
import urllib.request
from datetime import datetime
from db import db_api as db

UPLOADS_DIR = os.path.join('static', 'uploads')
IMAGE_DIR = os.path.join('static', 'images')
HASH_SALT = b'1U+q8L!TXEyws+5+OKEzf=q~ffCo>8-u/QJyL}cSqcg~~Ar`C{u{ZPP{Ky6M`l|b'
USER_COOKIE = "current_user"

def hash_string(s):
    return hashlib.sha512(HASH_SALT + s.encode()).hexdigest()

def get_upload_path(filename):
    return os.path.join(UPLOADS_DIR, filename)

def get_image_path(filename):
    return os.path.join(IMAGE_DIR, filename)

def get_current_time():
    return datetime.now().isoformat()

def get_secure_username(request):
    user_cookie = request.get_secure_cookie(USER_COOKIE)
    if user_cookie:
        user_cookie = user_cookie.decode("utf-8")
        user = db.User.find(username=user_cookie)
        if user is not None:
            return user.username
    return None

def fetch_file(url, filename):
    response = urllib.request.urlretrieve(url, filename)
    return response

#TODO: maybe move this to db_api instead?
def get_user_picture(userObj):
    return userObj.picture if userObj.picture is not None and userObj.picture != "" else "nouser.png"

def reply_malformed(request, header_text="The request was malformed", text="Sorry!\n It looks like your client has sent a invalid request.\n Please reload the page or contact us."):
    """Sets the header of request to 400 (bad request) and writes the text supplied"""
    request.set_status(400, header_text)
    request.write(text)