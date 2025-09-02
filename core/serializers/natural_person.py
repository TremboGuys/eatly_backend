from rest_framework.serializers import ModelSerializer, ValidationError

from core.models import NaturalPerson

from .serializer_helpers import make_user_active
from utils.helpers import verify_is_active

class NaturalPersonSerializer(ModelSerializer):
    class Meta:
        model = NaturalPerson
        fields = "__all__"
    
    def create(self, validated_data):
        person = make_user_active(validated_data=validated_data, instance=NaturalPerson)

        return person
    
    # def validate(self, attrs):
    #     if self.context['request'].method == "POST":
    #         if verify_is_active(attrs) == True:
    #             raise ValidationError({"error": "User is already active"})
        
    #     return attrs