#All from notes
import urllib.request
import base64
import math
from tkinter import PhotoImage

def downloadImage(image_path):
    import os, ssl
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    pic = urllib.request.urlopen(image_path)
    raw_data = pic.read()

    return base64.b64encode(raw_data)

def PhotoImageFromLink(link):
    base64_data = downloadImage(link)
    image = PhotoImage(data=base64_data)
    return image
