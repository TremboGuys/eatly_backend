from rest_framework import serializers

from django.contrib.auth.models import Group

from usuario.models import Usuario

class UserRegisterSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = []

    for x in Group.objects.all():
        ROLE_CHOICES.append(x.name)

    role = serializers.ChoiceField(choices=ROLE_CHOICES, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['email', 'password', 'role', 'is_active']
    
    def create(self, validated_data):
        role = validated_data.pop('role')

        user = Usuario.objects.create_user(**validated_data)

        try:
            group = Group.objects.get(name=role)
            user.groups.add(group)
        except:
            raise serializers.ValidationError({"role": "Group not found"})
        
        return user