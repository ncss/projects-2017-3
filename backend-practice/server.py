from tornado.ncss import Server, ncssbook_log

def index_handler(request):
    request.write("hello world")


server = Server()
server.register(r'/', index_handler)
server.run()