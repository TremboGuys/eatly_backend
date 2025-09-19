from rest_framework import serializers

from django.contrib.auth.models import Group

from usuario.models import Usuario


class UserRegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[], write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['email', 'password', 'role', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            group_choices = [(group.name, group.name) for group in Group.objects.all()]
        except Exception:
            group_choices = []
        
        self.fields['role'].choices = group_choices
    
    def create(self, validated_data):
        role = validated_data.pop('role')

        user = Usuario.objects.create_user(**validated_data)

        try:
            group = Group.objects.get(name=role)
            user.groups.add(group)
        except:
            raise serializers.ValidationError({"role": "Group not found"})
        
        return user

class ListUserSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()

    def get_group(self, obj):
        group = ""
        for g in obj.groups.all():
            group = g.name
        return group
    class Meta:
        model = Usuario
        fields = ['email', 'group']