from rest_framework.serializers import ModelSerializer, ValidationError

from core.models import Order, NaturalPerson
from utils.helpers import verify_group_user

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
    
    def validate(self, attrs):
        if ("client" in attrs and "deliveryMan" in attrs) and attrs["client"] == attrs["deliveryMan"]:
            raise ValidationError({"error": "Client and deliveryman can't have the same id"})
    
        if verify_group_user(NaturalPerson, attrs['client'], 'client') == False:
            raise ValidationError({"error": "Id client does not have the corresponding group"})
        
        if attrs.data['deliveryMan'] != None and verify_group_user(NaturalPerson, attrs['deliveryMan'], 'deliveryman') == False:
            raise ValidationError({"error": "Id deliveryman does not have the corresponding group"})
        
        return attrs