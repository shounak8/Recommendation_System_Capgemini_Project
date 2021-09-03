# Importing Image class from PIL module
from PIL import Image


def resize(path):
    # Opens a image in RGB mode
    im = Image.open(path)
    newsize = (400, 300)
    im1 = im.resize(newsize)
    im1.save(path)