from rest_framework import serializers

from django.contrib.auth.models import Group

from usuario.models import Usuario
from django.contrib.auth.hashers import make_password
from utils.helpers import create_image_user, update_image_user
from django.db import transaction


class UserRegisterSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False, allow_null=True)
    role = serializers.ChoiceField(choices=[], write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['email', 'password', 'role', 'is_active', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            group_choices = [(group.name, group.name) for group in Group.objects.all()]
        except Exception:
            group_choices = []
        
        self.fields['role'].choices = group_choices
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        file = validated_data.pop('file')

        user = Usuario.objects.create_user(**validated_data)

        try:
            group = Group.objects.get(name=role)
            user.groups.add(group)
        except:
            raise serializers.ValidationError({"role": "Group not found"})
        
        if file is not None:
            photo = create_image_user(file=file)
            user.photo = photo['secure_url']
            user.public_id_cloudinary = photo['public_id']

        user.save()
        
        return user

class UserRegisterGoogleSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)
    url_image = serializers.URLField(write_only=True)
    photo = serializers.URLField(required=False)
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'role', 'url_image', 'photo']
    
    def create(self, validated_data):
        with transaction.atomic():
            email = validated_data.pop('email', None)
            user = Usuario.objects.create_user(email=email, password=None)
            user.set_unusable_password()

            try:
                group = Group.objects.get(name=validated_data['role'])
                user.groups.add(group)
            except:
                raise serializers.ValidationError("Group not found!")
            
            if validated_data['url_image'] is not None:
                photo = create_image_user(validated_data['url_image'], image_is_url=True)
                user.photo = photo['secure_url']
                user.public_id_cloudinary = photo['public_id']
            
            user.save()

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

class UpdateUserSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    class Meta:
        model = Usuario
        fields = ['email', 'password', 'photo', 'file']
    
    def update(self, instance, validated_data):
        file = validated_data.get('file')
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        if instance.photo == "":
            photo = create_image_user(file=file)
            instance.photo = photo['secure_url']
            instance.public_id_cloudinary = photo['public_id']
        else:
            photo = update_image_user(file=file, public_id=instance.public_id_cloudinary)
            instance.photo = photo['secure_url']

        if email is not None:
            instance.email = validated_data['email']
        if password is not None:
            instance.password = make_password(validated_data['password'])

        instance.save()

        return instance