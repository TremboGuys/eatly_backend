import random
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.core.signing import Signer

from usuario.models import Usuario
from core.serializers import UserRegisterSerializer, TelephoneSerializer, ListUserSerializer, UpdateUserSerializer, ProfileNaturalPersonSerializer
from utils.helpers import send_email_register

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        with transaction.atomic():
            data = request.data.copy()
            data['file'] = request.FILES.get("file", None)
            serializerUser = UserRegisterSerializer(data=data)
            serializerUser.is_valid(raise_exception=True)
            user = serializerUser.save()

            signer = Signer()
            token = signer.sign(user.id)

            send_email_register(user.id, token)
            # transaction.on_commit(lambda: send_email_register.delay(user.id))

            return Response(data={"id": user.id}, status=status.HTTP_201_CREATED)

class CodeAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get('token', None)
        signer = Signer()

        if token is None:
            return Response(data={"error_code": "TOKEN_IS_NULL", "message": "Token not found!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            id = signer.unsign(token)
        except Exception as error:
            return Response(data={"error_code": "TOKEN_INVALID", "message": f"{error}"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = Usuario.objects.get(id=id)

        if user is None:
            raise Response(data={"error_code": "USER_NOT_EXIST", "message": "User not found!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_active:
            return Response(data={"error_code": "USER_ALREADY_ACTIVE", "message": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_active = True
            user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)


class UserListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user = self.request.user

        queryset = Usuario.objects.get(id=user.id)

        serializer = ListUserSerializer(queryset, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserUpdateAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        user = self.request.user
        file = request.FILES.get('file', None)
        data = request.data.copy()
        data['file'] = file

        serializer = UpdateUserSerializer(instance=user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileNaturalPersonAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = self.request.user
        print(user)

        queryset = Usuario.objects.get(id=user.id)

        serializer = ProfileNaturalPersonSerializer(queryset)

        return Response(data=serializer.data, status=status.HTTP_200_OK)