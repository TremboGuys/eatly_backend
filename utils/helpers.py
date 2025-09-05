from usuario.models import Usuario
from django.core.exceptions import ValidationError
from infra.cloudinary import UploadCloudinary

def verify_is_active(data):
    user = data.get('user')

    if user.is_active == 1:
        return True
    
    return False

def verify_group_user(instance, id_user, group):
    if id_user is not None:
        user = instance.objects.get(id=id_user)

        if user == None:
            return False
        
        if hasattr(user, 'user') == True:
            if user.user.groups.get(name=group):
                return True
        else:
            if user.groups.get(name=group):
                return True
    else:
        if instance.user.groups.get(name=group):
            return True
    return False

def create_image(file):
    uploader = UploadCloudinary()
    response = uploader.create_image(file=file)

    return response['secure_url']

def relate_user_group(user_data, id):
    if user_data.role == "client":
        from core.serializers import NaturalPersonSerializer

        npModel = {"name": user_data.pop('name'), "date_birth": user_data.pop('date_birth')}

        serializer = NaturalPersonSerializer(data=npModel)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
    if user_data.role == "restaurant":
        from core.serializers import RestaurantSerializer

        restaurantModel = {"name": user_data.pop('name'), "cnpj": user_data.pop('cnpj'), "average_delivery_time": user_data.pop('average_delivery_time'), "description": user_data.pop('description'), "categories": user_data.pop('categories')}

        serializer = RestaurantSerializer(data=restaurantModel)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
    if user_data == "deliveryman":
        from core.serializers import NaturalPersonSerializer

        
