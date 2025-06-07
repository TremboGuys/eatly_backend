from usuario.models import Usuario
from django.core.exceptions import ValidationError

def verify_is_active(data):
    print(data)
    user = Usuario.objects.get(id=data.get('user'))

    if user.is_active == 1:
        return True
    
    return False