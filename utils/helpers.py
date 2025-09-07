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
    if user_data['user']['role'] == "client":
        from core.serializers import NaturalPersonSerializer

        if "client" not in user_data:
            raise ValidationError({"error": "Client need their respective data!"})

        npModel = {"user": id, **user_data['client']}

        serializer = NaturalPersonSerializer(data=npModel)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return
    
    if user_data['user']['role'] == "restaurant":
        from core.serializers import CreateRestaurantSerializer

        if not all(field in user_data for field in ["address", "restaurant"]):
            raise ValidationError({"error": "Restaurant need their respective data!"})

        restaurantModel = {"user": id, **user_data['restaurant']}

        serializerRestaurant = CreateRestaurantSerializer(data=restaurantModel)
        serializerRestaurant.is_valid(raise_exception=True)
        serializerRestaurant.save()

        user_data['address']['user'] = id

        createAddress(user_data['address'])
        return
    
    if user_data['user']['role'] == "deliveryman" or user_data['user']['role'] == "owner":
        from core.serializers import NaturalPersonSerializer

        if "address" not in user_data:
            raise ValidationError({"error": "Deliveryman or Owner need address!"})
        
        if all(field in user_data for field in ["document_type", "document_number", "document_country"]):
            raise ValidationError({"error": "Deliveyrman or Owner need their respective data!"})
        
        if user_data['user']['role'] == 'deliveryman' and user_data['natural_person']['document_type'] != 'CNH':
            raise ValidationError({"error": "Deliveryman needs CNH"})
        
        user_data['natural_person']['user'] = id

        serializer = NaturalPersonSerializer(data=user_data['natural_person'])
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data['address']['user'] = id

        createAddress(user_data['address'])
        return

def createAddress(address):
    from core.serializers import AddressSerializer

    serializerAddress = AddressSerializer(data=address)
    serializerAddress.is_valid(raise_exception=True)
    serializerAddress.save()