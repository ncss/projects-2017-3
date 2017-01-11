from auth import requires_login
from backend.common import *
from template_engine import render

UP_IMAGES = []
@requires_login
def ask_handler(request):
    name = request.get_field("name")
    request.write(render("ask.html", {'username': 'rand'}))

@requires_login
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