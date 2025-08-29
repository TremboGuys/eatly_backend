from usuario.models import Usuario
from django.core.exceptions import ValidationError
from infra.cloudinary import UploadCloudinary

def verify_is_active(data):
    user = data.get('user')

    if user.is_active == 1:
        return True
    
    return False

def verify_group_user(instance, id_user, group):
    user = instance.objects.get(id=id_user)

    if user == None:
        return False
    
    if hasattr(user, 'user') == True:
        if user.user.groups.get(name=group):
            return True
    else:
        if user.groups.get(name=group):
            return True
    return False

def create_image(file):
    uploader = UploadCloudinary()
    response = uploader.create_image(file=file)

    return response['secure_url']