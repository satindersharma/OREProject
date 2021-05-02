
import qrcode
from django.core.files.base import ContentFile
from qrcode.image.svg import SvgPathImage

#  ---------------------------------------------------------------
# qr_code_generator
#  ---------------------------------------------------------------
def qr_code_generator(qr_code_info):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_info)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    return img


def qr_code_svg_generator(qr_code_info):
    
    svg_img = qrcode.make(qr_code_info, 
        version=1,
        box_size=10,
        border=1,
        image_factory=SvgPathImage,
        )
        
    # svg_img.save('qrcode00141.svg')

    return svg_img

def get_content(content,name):
    return ContentFile(content=content, name=name)