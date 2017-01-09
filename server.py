from tornado.ncss import Server, ncssbook_log

def index_handler(request):
    request.write("hello there")

    param_name = request.get_field("name")
    if param_name != None:
        request.write("<br>")
        request.write(param_name)

    request.write("!")
def book_handler(request, book_id):
    request.write(book_id)


server = Server()
server.register(r'/', index_handler)
server.register(r'/book/(\d+)/?', book_handler)
server.run()
