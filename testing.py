from template_engine.parser import render
from tornado.ncss import Server, ncssbook_log
def handler(request):
    request.write(render("test.html", {'test': enumerate(range(10))}))

server = Server()
server.register(r'/test', handler)

server.run()
