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


server = Server()
server.register(r'/', index_handler)
server.run()
