from auth import requires_login
from backend.common import *
from template_engine import render
from db import db_api as db



def view_question_handler(request, question_id):
    try:
        post = db.Post.find(question_id)
        post_info = {'user' : post.user_id, 'description' : post.description, 'question' : post.title, 'date' : post.date, 'file' : post.files}
        print(post.title)
        #question = {'title': title, 'description': description}
        request.write(render('view_question.html', post_info))
    except:
        request.write('Invalid Id')
