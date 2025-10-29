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
            raise APIException(f'Error uploading image: {error}')

        return im
    
    def create_image_user(self, file, image_is_url=False):
        if not image_is_url:
            base64_image = image_to_base64(file)

        try:
            if image_is_url:
                im = cloudinary.uploader.upload(file, transformation=[{'width': 100, 'height': 80, 'crop': "scale"}])
            else:
                im = cloudinary.uploader.upload(base64_image, transformation=[{'width': 100, 'height': 80, 'crop': "scale"}])
        except Exception as error:
            raise APIException(f'Error uploading image of user: {error}')

        return im
    
    def update_image(self, file, public_id):
        base64_image = image_to_base64(file=file)

        try:
            im = cloudinary.uploader.upload(base64_image, public_id=public_id)
        except Exception as error:
            raise APIException(f'Error updating image: {error}')
        
        return im
    
    def update_image_user(self, file, public_id, image_is_url=False):
        if not image_is_url:
            base64_image = image_to_base64(file)

        try:
            if image_is_url:
                im = cloudinary.uploader.upload(image_is_url, public_id=public_id, transformation=[{'width': 100, 'height': 80, 'crop': "scale"}])
            else:
                im = cloudinary.uploader.upload(base64_image, public_id=public_id, transformation=[{'width': 100, 'height': 80, 'crop': "scale"}])
        except Exception as error:
            raise APIException(f'Error updating image of user: {error}')

        return im
    def create_pdf(self, file):
        verify_pdf(file=file)

        try:
            pdf = cloudinary.uploader.upload(file, unique_filename=False)
        except Exception as error:
            raise APIException(f'Error uploading pdf: {error}')
        return pdf
    
    def update_pdf(self, file, public_id):
        verify_pdf(file=file)

        try:
            pdf = cloudinary.uploader.upload(file, public_id=public_id, unique_filename=True)
        except Exception as error:
            raise APIException(f'Error updating PDF: ', { error })
        return pdf