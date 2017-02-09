from PIL import Image
import base64
from io import BytesIO
import imghdr
import binascii

class ImageWrapper:
    def __init__(self, img, type):
        self.img = img
        self.type = type
    
    def __str__():
        return "ImageWrapper Object of type " + self.type + "size: " + len(self.img)


INVALID_IMAGE = 'INVALID_IMAGE'
iconsize = 256

def is_image(img):
    print(ImageWrapper, Image)
    return (isinstance(img, ImageWrapper) and isinstance(img.img, Image.Image)) or isinstance(img, Image.Image) 


def open_image(data, change_icon=False, b64=False):
    """Returns an image object, given image binary data (gotten from request.get_file) """

    if b64:
        try:
            with open('out.txt', 'w') as f:
                f.write(data[22:])
            data = base64.b64decode(data[22:] if data.startswith("data:image/png;base64,") else data)
        except binascii.Error:
            print("unable to decode b64!")
            return INVALID_IMAGE

    io = BytesIO(data)

    with open("hi.png", 'wb') as f:
        import copy
        for i in (copy.deepcopy(io)):
            f.write(i)

    image_type = imghdr.what(io)
    if image_type:
        if change_icon:
            return ImageWrapper(to_icon(Image.open(io)), image_type)
        else:
            return ImageWrapper(Image.open(io), image_type)
    else:
        return INVALID_IMAGE


def to_icon(img):
    """Takes an Image object, and mutates it into a thumbname with the size iconsize"""
    reducerate = 1 # the ratio to times the img height and width
    if max(img.height, img.width) > iconsize:
        reducerate = 256 / max(img.height, img.width)

    return img.resize((int(img.width*reducerate), int(img.height*reducerate)), Image.ANTIALIAS)
