from auth import requires_login
from backend.common import *
from template_engine import render
from db import db_api as db
from auth import requires_login, authenticate_cookie


def view_question_handler(request, question_id):
    # try:
    post = db.Post.find(question_id)
    post_info = {
        'user': post.user_id,
        'description': post.description,
        'question': post.title,
        'date': post.date,
        'file': post.file,
        'signed_in': authenticate_cookie(request),
        'username': get_username(request),
        'comments': post.all_comments(),
        'user_ids': db.User.find_multiple(),
        'photo_id': post.id,
    }
    print(post.title)
    request.write(render('view_question.html', post_info))
    # except Exception as e:
        # print(e.with_traceback)
        # request.write('Invalid Id')
