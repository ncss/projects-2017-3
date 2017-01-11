from typing import Callable
from template_engine.parser import render
from db import db_api as db

USER_COOKIE = "current_user"

ALL_USER = {} # username : USER (object)

def authenticate_cookie(request):
    """Returns True if cookies can be authenicated"""
    user_cookie = request.get_secure_cookie(USER_COOKIE)
    if user_cookie:
        user_cookie = user_cookie.decode("utf-8")
        print(user_cookie)
        user = db.User.find(user_cookie)  # type: User
        if user is not None:
            print('user_cookie in alluser')
            return True
    return False

def render_no_login(request):
    request.write(render('notsignedin.html', {}))

def requires_login(func: Callable):
    """
    Function decorator for requiring login
    """
    def ret(response, *args, **kwargs):
        if authenticate_cookie(response):
            # noinspection PyCallingNonCallable
            return func(response, *args, **kwargs)
        else:
            return render_no_login(response)
    return ret



@requires_login
def foo(request, *args, **kwargs):
    print(request)
