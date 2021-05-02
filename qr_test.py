import qrcode
from qrcode.image.svg import SvgPathImage
import django
import uuid
from sys import argv
import os
from random import randint
from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
from io import BytesIO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OREProject.settings')
django.setup()
# lower the error correction level, the more information that can be stored, but the harder the code is to recognize for readers

def test_qr():
        
    # Link for website
    # input_data = f"https://satyam.pythonanywhere.com/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples-{randint(1,99999)}/"
    # input_data=f"https://satyam.pythonanywhere.com/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples-{randint(1,99999)}/"
    input_data=f"https://satyam.pythonanywhere.com/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples-{randint(1,99999)}/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples-{randint(1,99999)}/"
    print("Input Data length: ",len(input_data))
    #Creating an instance of qrcode
    qr = qrcode.QRCode(
            version=1,
            box_size=5,
            border=1)

    qr.add_data(input_data)

    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    print(type(img))
    print(type(img._img))

    assert isinstance(img,qrcode.image.pil.PilImage), "Not Image instance"
    assert isinstance(img._img,Image.Image), "Not a Pillow Image instance"

    img_size = img._img.size
    print("Barcode Image pixel size: ",img_size)
    fname = str(uuid.uuid1()) + '.png'
    print(fname)
    b = BarcodeImage(url=input_data)
    # print(img._img.tobytes())
    buffer = BytesIO()
    try:
        img.save(buffer)
        b.image.save(fname, File(buffer),save=True)
    finally:
        img.close()
    print("Image size: {:,.1f} KB".format(b.image.size/1024.0))
    print("===========")

def test_qr_old():
        
    # Link for website
    input_data = f"https://satyam.pythonanywhere.com/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples-{randint(1,99999)}/"
    # input_data=f"https://satyam.pythonanywhere.com/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples-{randint(1,99999)}/"
    # input_data=f"https://satyam.pythonanywhere.com/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples-{randint(1,99999)}/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples/blog/being-able-debug-great-tool-when-learning-new-programming-content-tutorial-will-facilitate-how-debug-using-visual-studio-vs-code-which-can-be-used-all-code-samples-{randint(1,99999)}/"
    print("Input Data length: ",len(input_data))
    #Creating an instance of qrcode

    qr = qrcode.QRCode(
            version=1,
            box_size=5,
            border=1)

    qr.add_data(input_data)

    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    # print(dir(img))
    # canvas = Image.new('RGB', (340, 340), 'white')
    img_size = img._img.size
    print("Barcode Image pixel size: ",img_size)
    canvas = Image.new('RGB', img_size , 'white')
    draw = ImageDraw.Draw(canvas)
    canvas.paste(img)
    fname = str(uuid.uuid1()) + '.png'
    buffer = BytesIO()
    canvas.save(buffer, 'PNG')

    # self.qr_code.save(fname, File(buffer), save=False)
    b = BarcodeImage(url=input_data)
    b.image.save(fname, File(buffer),save=True)
    canvas.close()



if __name__ == '__main__':
    from users.models import BarcodeImage
    test_qr()
    # test_qr_old()