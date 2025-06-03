from rest_framework.serializers import ModelSerializer

from core.models import Telephone

class TelephoneSerializer(ModelSerializer):
    class Meta:
        model = Telephone
        fields = "__all__"