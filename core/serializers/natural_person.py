from rest_framework.serializers import ModelSerializer

from core.models import NaturalPerson

from .serializer_helpers import make_user_active

class NaturalPersonSerializer(ModelSerializer):
    class Meta:
        model = NaturalPerson
        fields = "__all__"
    
    def create(self, validated_data):
        person = make_user_active(validated_data=validated_data, instance=NaturalPerson)

        return person