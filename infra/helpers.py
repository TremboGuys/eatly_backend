import base64
from PIL import Image

def image_to_base64(file):
    file_content = file.read()

    image = Image.open(file)
    image.verify()

    if image.format not in ["JPEG", "JPG", "PNG"]:
        raise TypeError("Invalid image format")
    
    base64_file = base64.b64encode(file_content).decode('utf-8')

    return f"data:image/{image.format.lower()};base64,{base64_file}"

def verify_pdf(file):
    if file._get_name()[-4:] != ".pdf":
        raise TypeError("Invalid file format")