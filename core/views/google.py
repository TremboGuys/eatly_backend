import os
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from infra.google import verify_google_token
from usuario.models import Usuario
from core.serializers import UserRegisterGoogleSerializer, NaturalPersonSerializer
from django.db import transaction

from dotenv import load_dotenv

load_dotenv()

class UserCreateByGoogleTokenAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        with transaction.atomic():
            token = request.data.get("token", None)

            if token is None:
                raise ValidationError("Access Token not found!")
            user_info = verify_google_token(request.data['token'])

            user = {
                "email": user_info['email'],
                "url_image": user_info['picture'],
                "role": request.data['role']
            }

            serializerUser = UserRegisterGoogleSerializer(data=user)
            serializerUser.is_valid(raise_exception=True)
            serializerUser.save()
            user = serializerUser.data

            natural_person = {
                "user": user['id'],
                "name": user_info['name']
            }

            serializerNp = NaturalPersonSerializer(data=natural_person)
            serializerNp.is_valid(raise_exception=True)
            serializerNp.save()

            user_instance = Usuario.objects.get(id=user['id'])

            refresh = RefreshToken.for_user(user=user_instance)

            data = {**user, "name": serializerNp.data['name'], "access": str(refresh.access_token), "refresh": str(refresh)}

            return Response(data=data, status=status.HTTP_201_CREATED)

class LoginByGoogleAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get("token", None)

        if token is None:
            raise ValidationError("Access Token not found!")
        user_info = verify_google_token(request.data['token'])

        try:
            user = Usuario.objects.get(email=user_info['email'])
            refresh = RefreshToken.for_user(user)

            data = {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            raise ValidationError(f"User not found: {error}")