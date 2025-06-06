from usuario.models import Usuario
from django.core.exceptions import ValidationError

def verify_role_register(data):
    print(data)
    user = Usuario.objects.get(id=data.get('user'))

    if user.role_register == 1:
        return False
    
    return True