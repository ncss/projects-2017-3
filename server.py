import os
from tornado.ncss import Server, ncssbook_log
from template_engine.parser import render
from backend import ask, user
from db import db_api as db
from auth import User, requires_login, add_user
TEMPLATE_DIR = 'templates'
UPLOADS_DIR = os.path.join('static', 'uploads')
IMAGE_DIR = os.path.join('static', 'images')

UP_IMAGES = []

def index_handler(response):
    print(UP_IMAGES)
    response.write(render('index.html', {'posts':UP_IMAGES})) # { 'post1': (image location, comment}


def handle_list_users(request):
    request.write(render('list_users.html', {'users': db.User.find_multiple()}))


def view_question_handler(response, question_id):
    title = response.get_field('title')
    description = response.get_field('description')
    question = {'title': title, 'description': description}
    response.write(render('view_question.html', {'question' : question_id}))



server = Server()
server.register(r'/', index_handler)
server.register(r'/view/(\d+)/?', view_question_handler)
server.register(r'/signup', user.signup_handler, post=user.signup_handler_post)
server.register(r'/ask',    ask.ask_handler,     post=ask.ask_handler_post)
server.register(r'/signin', user.signin_handler, post=user.signin_handler_post)
server.register(r'/logout', user.signout_handler)
server.register(r'/list_users', handle_list_users)

server.run()
