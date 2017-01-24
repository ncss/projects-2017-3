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
        user =  db.User.find_by_username(user_cookie)
        if user is not None:
            return user.username
    return None

def fetch_file(url, filename):
    response = urllib.request.urlretrieve(url, filename)
    return response

