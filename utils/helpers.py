from usuario.models import Usuario
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from infra.cloudinary import UploadCloudinary

def verify_is_active(data):
    user = data.get('user')

    if user.is_active == 1:
        return True
    
    return False

def verify_group_user(user, group):
    if user.groups.filter(name=group).exists():
        return True
    return False

def create_image(file):
    uploader = UploadCloudinary()
    response = uploader.create_image(file=file)

    return response

def create_image_user(file, image_is_url=False):
    uploader = UploadCloudinary()
    response = uploader.create_image_user(file=file, image_is_url=image_is_url)

    return response

def update_image(file, public_id):
    uploader = UploadCloudinary()
    response = uploader.update_image(file=file, public_id=public_id)

    return response

def update_image_user(file, public_id, image_is_url=False):
    uploader = UploadCloudinary()
    response = uploader.update_image_user(file=file, public_id=public_id, image_is_url=image_is_url)

    return response

def create_pdf(file):
    uploader = UploadCloudinary()
    response = uploader.create_pdf(file=file)

    return response

def update_pdf(file, public_id):
    uploader = UploadCloudinary()
    response = uploader.update_pdf(file=file, public_id=public_id)

    return response

def send_email_register(id, token):
    user = Usuario.objects.get(id=id)
    send_mail(
        subject="Código de verificação Eatly",
        message=f"Acesse esse link para registrar sua conta em nossa plataforma: http://localhost:5173/verify-email?token={token}",
        from_email="joaovictor239090@gmail.com",
        recipient_list=[user.email],
        fail_silently=False
    )