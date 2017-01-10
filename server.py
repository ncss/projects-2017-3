import os
from tornado.ncss import Server, ncssbook_log
from template_engine.parser import render
from auth import User, requires_login, add_user


TEMPLATE_DIR = 'templates'
UPLOADS_DIR = os.path.join('static', 'uploads')
IMAGE_DIR = os.path.join('static', 'images')

UP_IMAGES = []

def get_upload_path(filename):
    return os.path.join(UPLOADS_DIR, filename)

def get_image_path(filename):
    return os.path.join(IMAGE_DIR, filename)

def index_handler(response):
    print(UP_IMAGES)
    response.write(render('index.html', {'posts':UP_IMAGES})) # { 'post1': (image location, comment}

def signup_handler_post(request):
    ident = request.get_field('id')
    username = request.get_field('username')
    nickname = request.get_field('nickname')
    password = request.get_field('password')
    email = request.get_field('email')
    gender = request.get_field('gender')
    dob = request.get_field('dob')
    profile_pic = request.get_file('profile_picture')
    if profile_pic != (None, None, None):
        filename, content_type, data = profile_pic
        with open(get_upload_path(filename), 'wb') as f:
            f.write(data)
    else:
        print('It failed')
    if username != None:
        request.set_secure_cookie("current_user", username)
    user = User(ident, username, password, nickname, email, gender, dob, None, None)
    add_user(user)


#@requires_login
def ask_handler(request):
    name = request.get_field("name")
    request.write(render("ask.html", {'username': 'rand'}))

#@requires_login
def ask_handler_post(request):
    file = request.get_file('fileupload')
    question = request.get_field("question")
    #print(file)
    if file != (None, None, None):
        with open(get_image_path(file[0]), 'wb') as f:
            f.write(file[2])
            print("uploaded")
            UP_IMAGES.append({'image':file[0], 'question':question})
    else:
        print("upload failed")
    request.write("Your image was uploaded! name=%s"%(file[0]))
    request.redirect('/')

def signup_handler(request):
    request.write(render('signup.html', {}))
    ident = request.get_field('id')
    username = request.get_field('username')
    email = request.get_field('email')
    password = request.get_field('password')
    doc = request.get_field('doc')
    gender = request.get_field('gender')
    dob = request.get_field('dob')
    if username != None:
        request.set_secure_cookie("current_user", username)

def view_question_handler(response, question_id):
    title = response.get_field('title')
    description = response.get_field('description')
    question = {'title': title, 'description': description}
    response.write(render('view_question.html', {'question' : question_id}))

def signin_handler(request):
    username = request.get_field('username')
    password = request.get_field('password')
    signin = {'username': username, 'password': password}
    request.write(render('signin.html', signin))

def signin_handler_post(request):
    pass

@requires_login
def signout_handler(response):
    response.clear_cookie('current_user')
    response.redirect('/')

server = Server()
server.register(r'/', index_handler)
server.register(r'/view/(\d+)/?', view_question_handler)

server.register(r'/signup', signup_handler, post = signup_handler_post)

server.register(r'/ask', ask_handler, post=ask_handler_post)

server.register(r'/logout', signout_handler)

server.register(r'/signin', signin_handler, post= signin_handler_post)



server.run()
