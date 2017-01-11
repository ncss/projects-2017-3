import os
from datetime import datetime
UPLOADS_DIR = os.path.join('static', 'uploads')
IMAGE_DIR = os.path.join('static', 'images')



def get_upload_path(filename):
    return os.path.join(UPLOADS_DIR, filename)

def get_image_path(filename):
    return os.path.join(IMAGE_DIR, filename)

def get_current_time():
    return datetime.now().isoformat()
