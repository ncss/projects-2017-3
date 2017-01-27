from auth import requires_login
from back_end.common import *
from template_engine import render
from os import path
from db import db_api as db
from auth import requires_login, authenticate_cookie


def view_question_handler(request, question_id):
    # try:
    post = db.Post.find(question_id)

    post_info = {
        'user': post.user,
        'user_picture': get_user_picture(post.user),
        'description': post.description,
        'question': post.title,
        'date': post.date,
        'file': post.file,
        'signed_in': authenticate_cookie(request),
        'username': get_secure_username(request),
        'comments': post.all_comments(),
        'user_ids': db.User.find(all=True),
        'photo_id': post.id,
    }

    if all(post_info['comments']):
        for comment in post_info['comments']:
            if comment.user:
                comment.profile_pic = get_user_picture(comment.user)
                print("",comment.profile_pic)

    request.write(render('view_question.html', post_info))
    # except Exception as e:
        # print(e.with_traceback)
        # request.write('Invalid Id')

def comment_handler_post(request, photo_id):
    text = request.get_field('addComment')
    print(text, 'gotten')
    user_cookie = request.get_secure_cookie(USER_COOKIE)
    if user_cookie is not None:
        user_cookie = user_cookie.decode()
        if db.User.find(username=user_cookie):
            print(user_cookie)
            user = db.User.find(username=user_cookie)
            user.create_comment(db.Post.find(photo_id), text, None)
            request.redirect("/view/" + str(photo_id))
    else:

        request.write("You're not logged in!")
