from tornado.ncss import Server, ncssbook_log

def index_handler(request):
    request.write("hello world")
def book_handler(request, book_id):
    request.write(book_id)


server = Server()
server.register(r'/', index_handler)
server.register(r'/book/(\d+)/?', book_handler)
server.run()
