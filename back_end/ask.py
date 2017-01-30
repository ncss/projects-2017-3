import time
from os import rename
from auth import requires_login
from back_end.common import *
from template_engine import render
from os import path
from db import db_api as db
from auth import requires_login, authenticate_cookie
import re
from mimetypes import guess_extension

@requires_login
def ask_handler(request):
    name = request.get_field("name")
    request.write(render("ask.html", {'signed_in': authenticate_cookie(request), 'username': get_secure_username(request), 'file_error_msg': ''}))

@requires_login
def ask_handler_post(request):
    photo_files = request.get_file("fileupload")
    filename, content_type, data = photo_files
    title = request.get_field("question")
    description = request.get_field("description")
    if photo_files != (None, None, None):
        if content_type.startswith('image/'):
            if request.get_secure_cookie("current_user") is None:
                raise Exception("Not logged in")
            user_id = request.get_secure_cookie("current_user").decode()
            photo_file_ext_regex = re.search(r'\.[a-zA-Z]+$', filename)
            photo_file_ext = photo_file_ext_regex.group(0)
            photo_dir = path.join('uploads', 'questions', str(db.Post.get_next_post_id()) + photo_file_ext)
            curuser = db.User.find(username=user_id)
            post = db.Post.create(curuser, description, title, photo_dir)
            print("LOG: New post created: ", post)
            print("LOG: Comments in post: ", post.all_comments())
            with open(path.join('static', photo_dir), 'wb') as f:
                f.write(data)
            request.write("Your image was uploaded! name=%s"%(photo_files[0]))
            request.redirect('/view/' + str(post.id))
        else:
            request.write(render("ask.html", {'signed_in': authenticate_cookie(request), 'username': get_secure_username(request), 'file_error_msg': 'Uploaded file type not supported.'}))
    else:
        request.write(render("ask.html", {'signed_in': authenticate_cookie(request), 'username': get_secure_username(request), 'file_error_msg': 'We couldn\'t find an uploaded file.'}))
        # user_id = request.get_secure_cookie("current_user")
        # tempfile_name = str(int(time.time()))
        # filename, response = fetch_file(url, tempfile_name)
        # filename = filename + guess_extension(response['Content-Type'])
        # filepath = get_upload_path(filename)
        # rename(tempfile_name, filepath)
        # db.Post.create(user_id, description, title, get_current_time(), filename)
        # request.redirect('/')



        # TODO Actually handle any errors of any kind???

        # TODO Put some handling of the edge case where neither photo nor URL is entered
        # request.write('We couldn\'t find an uploaded file.')
