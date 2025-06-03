import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from PIL import Image
from rest_framework.exceptions import APIException
from .helpers import file_to_base64

load_dotenv()

class UploadCloudinary:
    cloudinary.config(
        cloud_name = os.getenv('CLOUD_NAME'),
        api_key = os.getenv('API_KEY'),
        api_secret = os.getenv('API_SECRET'),
        secure=True
    )

    def create_image(self, file):
        print(file)

        base64_file = file_to_base64(file)

        try:
            im = cloudinary.uploader.upload(base64_file)
        except Exception as error:
            raise APIException(f'Upload error: {error}')

        return im