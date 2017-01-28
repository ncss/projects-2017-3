from auth import requires_login
from back_end.common import *
from template_engine import render
from os import path
from db import db_api as db
from auth import requires_login, authenticate_cookie


def view_question_handler(request, question_id):
    post = db.Post.find(question_id)

    post_info = {
        'post':post,
        'signed_in': authenticate_cookie(request),
        'username': get_secure_username(request),
        'comments': post.all_comments(),
        'photo_id': post.id,
        'join': os.path.join
        # pass the os.path.join object so i can use it!
    }

    request.write(render('view_question.html', post_info))

def comment_handler_post(request, photo_id):
    text = request.get_field('addComment')
    print(text, 'gotten')
    user_cookie = request.get_secure_cookie(USER_COOKIE)
    if user_cookie is not None:
        user_cookie = user_cookie.decode()
        if db.User.find(username=user_cookie):
            print(user_cookie)
            user = db.User.find(username=user_cookie)
            post = db.Post.find(photo_id)
            comment = user.create_comment(post, text, None, get_user_picture(user))
            request.redirect("/view/" + str(photo_id))
    else:

        request.write("You're not logged in!")
