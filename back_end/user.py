from auth import requires_login, USER_COOKIE, authenticate_cookie
from template_engine.parser import render
from back_end.common import *
from db import db_api as db

def signup_handler(request):
    request.write(render('signup.html', {'signed_in':authenticate_cookie(request), 'username': get_username(request)}))
    ident = request.get_field('id')
    username = request.get_field('username')
    email = request.get_field('email')
    password = request.get_field('password')
    doc = request.get_field('doc')
    gender = request.get_field('gender')
    dob = request.get_field('dob')
    if username is not None:
        request.set_secure_cookie("current_user", username)


def signup_handler_post(request):
    ident = request.get_field('id')
    username = request.get_field('username')
    nickname = request.get_field('nickname')
    password = hash_string(request.get_field('password'))
    email = request.get_field('email')
    gender = request.get_field('gender')
    dob = request.get_field('dob')
    profile_pic = request.get_file('profile_picture')
    print(username)
    if db.User.find(username=username) is not None:
        request.write("username already exists!")
        return
    new_user = db.User.sign_up(username, password, nickname, email)

    # Validation for uploaded image
    if profile_pic != (None, None, None):
        filename, content_type, data = profile_pic
        if content_type.startswith('image/'):
            file_path_profile_pic = os.path.join('static', 'uploads', 'user_image', str(new_user.id) +'.jpg')
            with open(file_path_profile_pic, 'wb') as f:
                f.write(data)
                new_user.picture = str(new_user.id)+'.jpg'

        else:
            request.write("Uploaded file type not supported.")
    else:
        request.write('We couldn\'t find an uploaded file.')

    if username is not None:
        request.set_secure_cookie("current_user", username)


    request.redirect('/')

def signin_handler(request):
    username = request.get_field('username')
    password = request.get_field('password')
    signin = {'username': username, 'password': password, 'signed_in':authenticate_cookie(request), 'username': get_username(request)}
    request.write(render('signin.html', signin))

def signin_handler_post(request):
    username = request.get_field('username')
    password = hash_string(request.get_field('password'))
    if db.User.find(username=username):
        if db.User.find(username=username).password == password:
            request.set_secure_cookie("current_user", username)
            user = db.User.find(username=username)
            request.redirect('/')
        else:
            request.write("The username and password do not match.")
    else:
        request.write("Username cannot be found.")
        return(None)

@requires_login
def signout_handler(request):
    request.clear_cookie('current_user')
    request.redirect('/')
