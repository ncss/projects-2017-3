from tornado.ncss import Server, ncssbook_log
from tornado import web
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

def _404_handler(request):
    request.write(render('404.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request)}))

def _403_handler(request):
    request.write(render('403.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request)}))

def monkey_handler(request):
    request.write(render('monkey.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request)}))

def check_valid_question_id_handler(request, question_id):
    post = db.Post.find(question_id)
    if post is not None:
        view.view_question_handler(request, question_id)
    else:
        _404_handler(request)

def check_valid_profile_handler(request, username):
    user = db.User.find(username=username)
    if user is not None:
        profile.view_handler(request, username)
    else:
        _404_handler(request)

def exception_handler(request, httpcode, *args, **kwargs):
    """This handler should be called when an exception happens during code :(. So it doesnt leak the stacktrace"""
    try:
        request.write(render("internal_error.html", {"code":httpcode, 'signed_in': authenticate_cookie(request), 'username': get_secure_username(request)}))
    except:
        print("another exception was raised!", traceback.print_exc())

def default_handler(request, type, *args, **kwargs):
    """type is (GET, POST, PUT, PATCH, DELETE), request is reference to a request_handler"""
    _404_handler(request)


class CustomStaticFileHandler(web.StaticFileHandler):
    """Static handler that shows an error message"""
    def validate_absolute_path(self, root, absolute_path):
        try:
            return super().validate_absolute_path(root, absolute_path)
        except web.HTTPError as e:
            if e.status_code == 403: # permission denied, probably a directory
                self.set_status(403)
                _403_handler(self)
                return None
            elif e.status_code == 404: # doesnt exist!
                self.set_status(404)
                _404_handler(self)
            else:
                raise



server = Server(default_handler=default_handler, default_write_error=exception_handler, static_handler_class=CustomStaticFileHandler) # sets the default exception handler
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
server.register(r'/ajax/user_validate'  , _404_handler                , post=ajax.username_handler    )
server.register(r'/ajax/email_validate' , _404_handler                , post=ajax.email_handler       )
server.register(r'/ajax/logged_in_validate' , _404_handler            , post=ajax.user_logged_in_handler)


server.register(r'/monkey'      , monkey_handler)
server.run()
