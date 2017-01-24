from typing import Callable
from template_engine.parser import render
from db import db_api as db
from back_end.common import get_secure_username

USER_COOKIE = "current_user"

ALL_USER = {} # username : USER (object)
ADMINS = [db.User.find(id=x).username for x in range(1,12)] # sets the first 10 people to be site? admins
# temporary

def authenticate_cookie(request):
    """Returns True if cookies can be authenicated"""
    user_cookie = request.get_secure_cookie(USER_COOKIE)
    if user_cookie:
        user_cookie = user_cookie.decode("utf-8")
        print(user_cookie)
        user = db.User.find(username=user_cookie)  # type: User
        if user is not None:
            print('user_cookie in alluser')
            return True
    return False

def render_no_login(request):
    request.write(render('notsignedin.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request)}))

def requires_login(func: Callable):
    """
    Function decorator for requiring login
    """
    def ret(request, *args, **kwargs):
        if authenticate_cookie(request):
            # noinspection PyCallingNonCallable
            return func(request, *args, **kwargs)
        else:
            return render_no_login(request)
    return ret

def require_specific_user(func):
    """Decorator that requires the user to = to the cookie set in request"""
    def ret(request, username, *args, **kwargs):
        if authenticate_correct_username(request, username):
            return func(request,username, *args, **kwargs)
        else:
            request.write("you cannot edit someone else's profile you hacker!")
    return ret

def authenticate_correct_username(request, username):
    user_cookie = request.get_secure_cookie(USER_COOKIE)
    if user_cookie:
        user_cookie = user_cookie.decode("UTF-8")
        return user_cookie == username
    else:
        return False

def requires_admin(func):
    def ret(request, *args, **kwargs):
        if authenticate_admin(request):
            return func(request, *args, **kwargs)
        else:
            request.write("You cannot access this unless your an admin. (try log in, else delete the decorator in server.py")
    return ret

def authenticate_admin(request):
    username = request.get_secure_cookie(USER_COOKIE)
    return username is not None and username.decode("UTF-8") in ADMINS
