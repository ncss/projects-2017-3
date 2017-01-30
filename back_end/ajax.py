from db import db_api
from back_end.common import reply_malformed, get_secure_username

USER_COOKIE = "current_user"

def username_handler(request):
    user = request.get_field("username")
    if isinstance(user, str):
        valid = db_api.User.find(username=user.lower())
        # checks if the user already signed up
        # if there is no user, it is valid
        valid = True if valid is None else False
        print(user, valid)
        request.write({"user_valid" : valid})
    else:
        reply_malformed(request)

def email_handler(request):
    email = request.get_field("email")
    if isinstance(email, str):
        valid = db_api.User.find(email=email.lower())
        valid = True if valid is None else False
        request.write({"email_valid" : valid})
    else:
        reply_malformed(request)

def user_logged_in_handler(request):
    user_cookie = request.get_secure_cookie(USER_COOKIE)
    if user_cookie is not None:
        print('user:', user_cookie.decode())
        is_logged_in = True
    else:
        is_logged_in = False
    request.write({"is_logged_in": is_logged_in})
