from db import db_api as db
from template_engine.parser import render
from backend.common import *
from auth import authenticate_cookie, requires_login, require_specific_user


@requires_login
@require_specific_user
def view_handler(request, username):
    user = db.User.find_by_username(username)
    if user is None:
        request.write("username is not in db")
    else:
        request.write(render('profile.html', {'username':user.username, 'nickname': user.nickname,
                                        'email': user.email, 'picture':user.picture, 'signed_in':authenticate_cookie(request)}))

def view_handler_post(request, username):
    ... #we could use db.update here in the future
