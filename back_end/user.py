from auth import requires_login, USER_COOKIE, authenticate_cookie
from template_engine.parser import render
from back_end.common import *
from db import db_api as db

NOUSER_PROFILEPIC_FILENAME = 'nouser.png'

def signup_handler(request):
    request.write(render('signup.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request), 'unsupported_file_error_msg': ''}))
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
            file_path_profile_pic = os.path.join('uploads', 'user_image', str(new_user.id) +'.jpg')

            with open(os.path.join('static', file_path_profile_pic), 'wb') as f:
                f.write(data)
                db.User.update(new_user.id, new_user.password, new_user.nickname, new_user.email, new_user.gender, new_user.dob, new_user.bio, file_path_profile_pic)
                print(new_user.picture)
                request.redirect('/')

        else:
            print('Uploaded file type not supported')
            request.write(render('signup.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request), 'unsupported_file_error_msg': 'Uploaded file type not supported.'}))
    else:
        file_path_profile_pic = os.path.join('uploads', 'user_image', NOUSER_PROFILEPIC_FILENAME)
        db.User.update(new_user.id, new_user.password, new_user.nickname, new_user.email, new_user.gender, new_user.dob, new_user.bio, file_path_profile_pic)
        request.write('We couldn\'t find an uploaded file. So we\'ll assign you a default pic.')
        request.redirect('/')

    if username is not None:
        request.set_secure_cookie("current_user", username)



def signin_handler(request):
    if get_secure_username(request):
        # the user is already logged in!
        request.redirect('/')
    signin = {'signed_in':False, 'error_message': ''}
    request.write(render('signin.html', signin))

def signin_handler_post(request):
    username = request.get_field('username').lower()
    password = hash_string(request.get_field('password'))
    userObj = db.User.find(username=username)
    signin_error_message = ""
    if userObj:
        if userObj.password == password:
            request.set_secure_cookie("current_user", username)
            request.redirect('/')
        else:
            request.write(render('signin.html', {'signed_in':False, 'error_message': "The username and password do not match."}))
    else:
        request.write(render('signin.html', {'signed_in':False, 'error_message': "Username cannot be found in database."}))

@requires_login
def signout_handler(request):
    request.clear_cookie('current_user')
    request.redirect('/')
