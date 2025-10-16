from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from core.models import NaturalPerson

class NaturalPersonSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = NaturalPerson
        fields = "__all__"