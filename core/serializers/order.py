from rest_framework.serializers import ModelSerializer, ValidationError

from core.models import Order, NaturalPerson
from utils.helpers import verify_group_user

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
    
    def validate(self, attrs):
        deliveryMan = attrs.get('deliveryMan', None)
        client = attrs.get('client', None)
        if (client is not None and deliveryMan is not None) and client == deliveryMan:
            raise ValidationError({"error": "Client and deliveryman can't have the same id"})
    
        if verify_group_user(client, None, 'client') == False:
            raise ValidationError({"error": "Id client does not have the corresponding group"})
        
        if deliveryMan is not None and verify_group_user(deliveryMan, None, 'deliveryman') == False:
            raise ValidationError({"error": "Id deliveryman does not have the corresponding group"})
        
        return attrs