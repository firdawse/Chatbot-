import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen



im_1_path = 'https://api.twilio.com/2010-04-01/Accounts/AC3994386f98172efbcc045881d2c4703d/Messages/MM1b8f4f522c95c52f16fde8f6a25bf3e2/Media/ME778522a5f6d929efb798004d98b1da60'

def recognize_text(img_path):
    '''loads an image and recognizes text.'''
    req = Request(img_path, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    reader = easyocr.Reader(['en'])
    return reader.readtext(webpage)

result = recognize_text(im_1_path)
print(result[7][1])








