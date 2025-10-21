from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from core.models import Telephone

class TelephoneSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = Telephone
        fields = "__all__"