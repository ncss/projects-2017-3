from db import db_api as db

def view_handler(request, regex):
    user = db.User.find(regex)
    if user is None:
        request.write("username is imvalid")
    else:
        #pass [username, nickname, email, gender, dob, bio, picture]
        request.write(str(user.id)+ " " + user.username + " "+ user.nickname + " "+ user.email)
def view_handler_post(request, regex):
    ... #we could use db.update here in the future
