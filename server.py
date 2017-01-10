import os
from tornado.ncss import Server, ncssbook_log

TEMPLATE_DIR = 'templates'


def render_file(response, filename:str, variables) -> None:
    """Renders the filename replaceing {name} with keys in variables"""
    response.write(get_template(filename).format(**variables))


def get_template(filename):
    """
    Gets the template from TEMPLATE_DIR with name filename
    """
    with open(os.path.join(TEMPLATE_DIR, filename)) as f:
        return f.read()

def index_handler(response):
    render_file(response, 'index.html', {})

def ask_handler(request):
    name = request.get_field("name")
    render_file(request, "ask.html", {'username':str(name)})

def ask_handler_put(request):
    ...

def signup_handler(request):
    render_file(request, 'signup.html', {})
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
    render_file(response, 'view_question.html', question)

def signout_handler(response):
    response.clear_cookie('current_user')
    response.redirect('/')

server = Server()
server.register(r'/', index_handler)
server.register(r'/view/(\d+)/?', view_question_handler)
server.register(r'/signup', signup_handler)
server.register(r'/ask', ask_handler)
server.register(r'/signout', signout_handler)
server.run()
