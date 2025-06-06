from rest_framework.serializers import ModelSerializer

from core.models import Client

from .serializer_helpers import make_user_active

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
    
    def create(self, validated_data):
        client = make_user_active(validated_data=validated_data, instance=Client)

        return client