from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from core.models import Address

class AddressSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Address
        fields = "__all__"