from auth import requires_login
from backend.common import *
from template_engine import render
from db import db_api as db

@requires_login
def ask_handler(request):
    name = request.get_field("name")
    request.write(render("ask.html", {'username': 'rand'}))

@requires_login
def ask_handler_post(request):
    photo_files = request.get_file("fileupload")
    title = request.get_field("question")
    description = request.get_field("description")
    if photo_files != (None, None, None):
        user_id = request.get_secure_cookie("current_user")
        '''photo_files from database needs to be discussed regarding single/multiple photo uploads'''
        db.Post.create(user_id, description, title, get_current_time(), [photo_files[2]])
    else:
        print("upload failed")
    request.write("Your image was uploaded! name=%s"%(photo_files[0]))
    request.redirect('/')
