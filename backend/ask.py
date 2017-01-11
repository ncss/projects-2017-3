from auth import requires_login
from backend.common import *
from template_engine import render
from os import path
from db import db_api as db
from auth import requires_login, authenticate_cookie
import re

@requires_login
def ask_handler(request):
    name = request.get_field("name")
    request.write(render("ask.html", {'username': 'rand', 'signed_in':authenticate_cookie(request)}))

@requires_login
def ask_handler_post(request):
    photo_files = request.get_file("fileupload")
    filename, content_type, data = photo_files
    title = request.get_field("question")
    description = request.get_field("description")
    if photo_files != (None, None, None):
        if content_type.startswith('image/'):
            user_id = request.get_secure_cookie("current_user")
            photo_file_ext_regex = re.search(r'\.[a-zA-Z]+$', filename)
            photo_file_ext = photo_file_ext_regex.group(0)
            photo_dir = path.join('uploads', 'questions', db.Post.get_next_post_id() + photo_file_ext)
            post = db.Post.create(user_id, description, title, photo_dir)
            with open(path.join('static', photo_dir), 'wb') as f:
                f.write(data)
            request.write("Your image was uploaded! name=%s"%(photo_files[0]))
            request.redirect('/view/' + str(post.id))
        else:
            request.write("uploaded file type not supported")

    else:
        request.write('We couldn\'t find an uploaded file.')
