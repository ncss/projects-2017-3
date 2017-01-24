from db import db_api

def username_handler(request):
    print(request.get_field("username"))
    valid = db_api.User.find_by_username(request.get_field("username").lower())
    # checks if the user already signed up
    # if there is no user, it is valid
    valid = True if valid is None else False
    request.write({"user_valid" : valid})
