import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from PIL import Image
from rest_framework.exceptions import APIException
from .helpers import image_to_base64, verify_pdf

load_dotenv()

class UploadCloudinary:
    cloudinary.config(
        cloud_name = os.getenv('CLOUD_NAME'),
        api_key = os.getenv('API_KEY'),
        api_secret = os.getenv('API_SECRET'),
        secure=True
    )

    def create_image(self, file):
        base64_image = image_to_base64(file)

        try:
            im = cloudinary.uploader.upload(base64_image)
        except Exception as error:
            raise APIException(f'Upload error: {error}')

        return im
    
    def create_pdf(self, file):
        verify_pdf(file=file)

        try:
            pdf = cloudinary.uploader.upload(file, use_filename=True, unique_filename=False)
        except Exception as error:
            raise APIException(f'Upload error: {error}')
        return pdf