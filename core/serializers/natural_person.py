from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from core.models import NaturalPerson

# For cases where it is not possible to get SimpleJWT Token
class CreateUpdateNaturalPersonSerializer(ModelSerializer):
    class Meta:
        model = NaturalPerson
        fields = "__all__"

class NaturalPersonSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = NaturalPerson
        fields = "__all__"