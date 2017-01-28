from db import db_api
from back_end.common import reply_malformed

def username_handler(request):
    user = request.get_field("username")
    if isinstance(user, str):
        valid = db_api.User.find(username=user.lower())
        # checks if the user already signed up
        # if there is no user, it is valid
        print(user, valid)
        valid = True if valid is None else False
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