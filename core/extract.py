from pytesseract import image_to_string
from PIL import Image

def img_to_text(file):
    image = Image.open(file)
    text = image_to_string(image)
    return text