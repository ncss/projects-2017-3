from auth import requires_login
from backend.common import *
from template_engine import render
from db import db_api as db
from auth import requires_login, authenticate_cookie


def view_question_handler(request, question_id):
    #try:
        post = db.Post.find(question_id)

        post_info = {'user' : post.user_id, 'description' : post.description, 'question' : post.title, 'date' : post.date, 'file' : post.files[0][0], 'signed_in':authenticate_cookie(request)}
        #print(post.files[0][0])
        request.write(render('view_question.html', post_info))
