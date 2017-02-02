from PIL import Image
import base64
from io import BytesIO
import imghdr


iconsize = 256

def open_image(data, b64=False):
    """Returns an image object, given image binary data (gotten from request.get_file) """
    if b64:
        data = base64.b64decode(data)

    io = BytesIO(data)

    image_type = imghdr.what(io)
    if image_type:
        return (Image.open(io), image_type)
    else:
        return None


def to_icon(img):
    """Takes an Image object, and mutates it into a thumbname with the size iconsize"""
    reducerate = 1 # the ratio to times the img height and width
    if max(img.height, img.width) > iconsize:
        reducerate = 256 / max(img.height, img.width)

    return img.resize((int(img.width*reducerate), int(img.height*reducerate)), Image.ANTIALIAS)
