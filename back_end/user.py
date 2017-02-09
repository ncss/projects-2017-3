from auth import requires_login, USER_COOKIE, authenticate_cookie
from template_engine.parser import render
from back_end.common import *
from db import db_api as db
from back_end import Imaging

NOUSER_PROFILEPIC_FILENAME = 'nouser.png'

def signup_handler(request):
    request.write(render('signup.html', {'signed_in':authenticate_cookie(request), 'username': get_secure_username(request), 'unsupported_file_error_msg': ''}))


def signup_handler_post(request):
    UnreadableImage = False

    image_type = request.get_field('image-location')

    if not image_type in ('profile_img_webcam', 'profile_img_upload', None):
        print("gotten image-type", image_type)
        reply_malformed(request)
        return
    else:
        # get the image
        if image_type == 'profile_img_webcam':
            # webcam
            print("reading from webcam")
            print(request.get_field('webcam-input'))
            image = Imaging.open_image(request.get_field('webcam-input'), change_icon=True, b64=True)
        elif image_type == 'profile_img_upload':
            # file upload
            print("Reading from file upload")
            image = Imaging.open_image(request.get_file('profile_picture')[2], change_icon=True, b64=False)
        else:
            print("No file received! img_type=", image_type)
            image = None
        # the picture is a ImageWrapper obj, None for no image, or Imaging.Invalid if it is invalid


    username = request.get_field('username')
    nickname = request.get_field('nickname')
    password = hash_string(request.get_field('password'))
    email = request.get_field('email')
    gender = request.get_field('gender')
    dob = request.get_field('dob')


    if db.User.find(username=username) is not None:
        request.write("username already exists!")
        return
        
    if image == Imaging.INVALID_IMAGE:
        # the image was invalid! send the form back to the user and dont sign'em up
        print("Image was invalid :(")
        ...
    else:
        new_user = db.User.sign_up(username, password, nickname, email)

        if image is None:
            request.set_secure_cookie("current_user", username)
            # no image was supplied, do nofin
            request.redirect('/')

        elif Imaging.is_image(image):
            ext = image.type
            
            file_path = os.path.abspath(os.path.join('static', 'uploads', 'user_image', str(new_user.id) + '.' + ext))
            print("Saving img to", file_path)
            image.img.save(file_path)
            db.User.update_some(picture=file_path)
            request.set_secure_cookie("current_user", username)
            request.redirect('/')

        else:
            raise ValueError("image cannot be " + str(image))






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
