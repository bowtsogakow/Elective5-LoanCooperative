import base64
import random
import string
import qrcode
from io import BytesIO

def generate_qr_code(data): 
    qr = qrcode.QRCode(
        version=1,  # Size of the QR code grid (1 is smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in the grid
        border=4,  # Thickness of the border
        )
        
    qr.add_data(data)
    qr.make(fit=True)

    # Optionally, customize the QR code style (color, logo, etc.)
    img = qr.make_image(fill="black", back_color="white")

    # Convert the image to a binary stream
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  
    img_base64 = base64.b64encode(img_byte_arr.read()).decode('utf-8')  

    return img_base64


def generate_random_string(length=8):
    # Generate a random string of the specified length
    characters = string.ascii_letters + string.digits  # Choose the characters you want
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string