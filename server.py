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

def index_handler(request):
    request.write("hello there")

def signup_handler(request):
    render_file(request, 'signup.html', {})
    ident = request.get_field('id')
    username = request.get_field('username')
    email = request.get_field('email')
    password = request.get_field('password')
    doc = request.get_field('doc')
    gender = request.get_field('gender')
    dob = request.get_field('dob')

server = Server()
server.register(r'/', index_handler)
server.register(r'/signup', signup_handler)
server.run()
