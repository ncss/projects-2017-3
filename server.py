from tornado.ncss import Server, ncssbook_log
import os
from template_engine.parser import render
from backend import ask, user, profile, view
from db import db_api as db
from auth import requires_login, authenticate_cookie
from backend.common import *

TEMPLATE_DIR = 'templates'
UPLOADS_DIR = os.path.join('static', 'uploads')
IMAGE_DIR = os.path.join('static', 'images')

UP_IMAGES = []

def index_handler(request):
    print(UP_IMAGES)
    request.write(render('index.html', {'posts':UP_IMAGES, 'signed_in':authenticate_cookie(request)})) # { 'post1': (image location, comment}


def handle_list_users(request):
    request.write(render('list_users.html', {'users': db.User.find_multiple(), 'signed_in':authenticate_cookie(request)}))



server = Server()
server.register(r'/', index_handler)
server.register(r'/view/(\d+)/?', view.view_question_handler)
server.register(r'/signup'      , user.signup_handler  , post=user.signup_handler_post)
server.register(r'/ask'         , ask.ask_handler      , post=ask.ask_handler_post)
server.register(r'/signin'      , user.signin_handler  , post=user.signin_handler_post)
server.register(r'/logout'      , user.signout_handler)
server.register(r'/list_users'  , handle_list_users)
server.register(r'/profile/(.+)', profile.view_handler)
server.run()
