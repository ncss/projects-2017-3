from auth import requires_login
from backend.common import *
from template_engine import render
from db import db_api as db
from auth import requires_login, authenticate_cookie


def view_question_handler(request, question_id):
    #try:
        post = db.Post.find(question_id)
<<<<<<< HEAD

    #    with open('out.txt', 'w') as w:
    #        w.write(str(post.files[0]))
        post_info = {'user' : post.user_id, 'description' : post.description, 'question' : post.title, 'date' : post.date, 'file' : post.files[0][0], 'signed_in':authenticate_cookie(request)}
        #print(post.files[0][0])
=======
        post_info = {'user' : post.user_id, 'description' : post.description, 'question' : post.title, 'date' : post.date, 'file' : post.file, 'signed_in':authenticate_cookie(request), 'username': get_username(request)}
        print(post.title)
>>>>>>> 07b1e1fd998efe5012df723a470a68e1410c53a1
        request.write(render('view_question.html', post_info))
    #except(ValueError):
        #request.write('Invalid Id')
