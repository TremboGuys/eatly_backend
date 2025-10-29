from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from core.models import Telephone

class CreateTelephoneSerializer(ModelSerializer):
    class Meta:
        model = Telephone
        fields = "__all__"

class TelephoneSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Telephone
        fields = "__all__"

class ProfileTelephoneSerializer(ModelSerializer):
    class Meta:
        model = Telephone
        fields = ['number_e164']