from usuario.models import Usuario
from django.core.exceptions import ValidationError

def verify_is_active(data):
    user = Usuario.objects.get(id=data.get('user'))

    if user.is_active == 1:
        return True
    
    return False

def verify_group_user(id_user, group):
    user = Usuario.objects.get(id=id_user)

    if user == None:
        return False
    
    if user.groups.get(name=group):
        return True
    return False