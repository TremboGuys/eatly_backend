from rest_framework import serializers

from usuario.models import Usuario

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['email', 'password']
    
    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user