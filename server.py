from tornado.ncss import Server, ncssbook_log
import os
from template_engine.parser import render
from back_end import ask, user, profile, view, ajax
from db import db_api as db
from auth import requires_login, authenticate_cookie
from back_end.common import *

TEMPLATE_DIR = 'templates'
UPLOADS_DIR = os.path.join('static', 'uploads')
IMAGE_DIR = os.path.join('static', 'images')

UP_IMAGES = []

def index_handler(request):
    posts = db.Post.find_all()
    if not posts: posts=[]
    posts = [{'image':i.file if i.file != [] else 'notfound.jpg',
                  'question':i.title, 'id': i.id} for i in posts]
    request.write(render('index.html',
            {'posts':posts,
            'signed_in':authenticate_cookie(request),
            'username': get_secure_username(request),
            'link': 'view/()'})) # { 'post1': (image location, comment}


def aboutus_handler(request):

    request.write(render('aboutus.html', {'users': db.User.find(all=True), 'signed_in':authenticate_cookie(request), 'username': get_username(request)}))

def handle_list_users(request):
    request.write(render('list_users.html', {'users': db.User.find(all=True), 'signed_in':authenticate_cookie(request), 'username': get_username(request)}))

def not_found_handler(request):
    request.write(render('404.html', {'users': db.User.find(all=True), 'signed_in':authenticate_cookie(request), 'username': get_username(request)}))

def monkey_handler(request):
    request.write(render('monkey.html', {'users': db.User.find_all(), 'signed_in':authenticate_cookie(request), 'username': get_secure_username(request)}))



server = Server()
server.register(r'/', index_handler)
server.register(r'/view/(\d+)/?', view.view_question_handler)
server.register(r'/signup'      , user.signup_handler  , post=user.signup_handler_post)
server.register(r'/ask'         , ask.ask_handler      , post=ask.ask_handler_post)
server.register(r'/signin'      , user.signin_handler  , post=user.signin_handler_post)
server.register(r'/post_comment/(\d+)/?', view.comment_handler_post, post=view.comment_handler_post)
server.register(r'/logout'      , user.signout_handler)
server.register(r'/list_users'  , handle_list_users)
server.register(r'/profile/(.+)', profile.view_handler, post=profile.view_handler_post)
server.register(r'/profile/edit/(.+)', profile.edit_handler, post=profile.edit_handler_post)
server.register(r'/aboutus'     , aboutus_handler)
server.register(r'/ajax/user_validate', not_found_handler, post=ajax.username_handler)
server.register(r'/ajax/email_validate', not_found_handler, post=ajax.email_handler)

server.register(r'/monkey'      , monkey_handler)
server.register(r'/.*'          , not_found_handler)
server.run()
