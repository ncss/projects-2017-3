from tornado.ncss import Server, ncssbook_log
import os
from template_engine.parser import render
from back_end import ask, user, profile, view, ajax
from db import db_api as db
from auth import requires_login, authenticate_cookie, requires_admin
import traceback
from back_end.common import *

TEMPLATE_DIR = 'templates'
UPLOADS_DIR = os.path.join('static', 'uploads')
IMAGE_DIR = os.path.join('static', 'images')


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
    request.write(render('aboutus.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request)}))

@requires_admin
def handle_list_users(request):
    request.write(render('list_users.html', {'users': db.User.find(all=True), 'signed_in':authenticate_cookie(request), 'username': get_secure_username(request)}))
    # users:db.User.find(all=True) is only required for list_users page, cuz we really dont want to be listing users on the other websites :D

def not_found_handler(request):
    request.write(render('404.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request)}))

def monkey_handler(request):
    request.write(render('monkey.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request)}))

def check_valid_question_id_handler(request, question_id):
    post = db.Post.find(question_id)
    if post is not None:
        view.view_question_handler(request, question_id)
    else:
        not_found_handler(request)

def check_valid_profile_handler(request, username):
    user = db.User.find(username=username)
    if user is not None:
        profile.view_handler(request, username)
    else:
        not_found_handler(request)

def exception_handler(request, httpcode, *args, **kwargs):
    """This handler should be called when an exception happens during code :(. So it doesnt leak the stacktrace"""
    try:
        request.write(render("internal_error.html", {"code":httpcode, 'signed_in': authenticate_cookie(request), 'username': get_secure_username(request)}))
    except:
        print("another exception was raised!", traceback.print_exc())

server = Server(default_write_error=exception_handler) # sets the default exception handler
#               URL                       GET                              POST
server.register(r'/'                    , index_handler                                                    )
server.register(r'/view/(\d+)/?'        , check_valid_question_id_handler                                  )
server.register(r'/signup'              , user.signup_handler              , post=user.signup_handler_post )
server.register(r'/ask'                 , ask.ask_handler                  , post=ask.ask_handler_post     )
server.register(r'/signin'              , user.signin_handler              , post=user.signin_handler_post )
server.register(r'/post_comment/(\d+)/?', view.comment_handler_post        , post=view.comment_handler_post)
server.register(r'/logout'              , user.signout_handler                                             )
server.register(r'/list_users'          , handle_list_users                                                )
server.register(r'/profile/(.+)'        , check_valid_profile_handler      , post=profile.view_handler_post)
server.register(r'/profile/edit/(.+)'   , profile.edit_handler             , post=profile.edit_handler_post)
server.register(r'/aboutus'             , aboutus_handler                                                  )
server.register(r'/ajax/user_validate'  , not_found_handler                , post=ajax.username_handler    )
server.register(r'/ajax/email_validate' , not_found_handler                , post=ajax.email_handler       )
server.register(r'/ajax/login_validate' , not_found_handler                , post=ajax.user_logged_in_handler)


server.register(r'/monkey'      , monkey_handler)
server.register(r'/.*'          , not_found_handler)
server.run()
