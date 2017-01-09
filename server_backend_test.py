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

    param_name = request.get_field("name")
    if param_name != None:
        request.write("<br>")
        request.write(param_name)

    request.write("!")
def book_handler(request, book_id):
    request.write(book_id)

def test_reader(request):
    template = get_template('test.html')
    fname = request.get_field('fname')
    lname = request.get_field('lname')
    food = request.get_field('food')
    user = {'fname': fname, 'lname': lname, 'food': food}
    render_file(request, 'test.html', user)

server = Server()
server.register(r'/', index_handler)
server.register(r'/book/(\d+)/?', book_handler)
server.register(r'/test', test_reader)
server.run()
