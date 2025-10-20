import random
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

from usuario.models import Usuario, EmailVerificationUser
from core.serializers import UserRegisterSerializer, EmailVerificationUserSerializer, TelephoneSerializer, ListUserSerializer, UpdateUserSerializer
from utils.helpers import send_email_register

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        with transaction.atomic():
            code = random.randint(100000, 999999)
            data = request.data.copy()
            data['file'] = request.FILES.get("file", None)
            serializerUser = UserRegisterSerializer(data=data)
            serializerUser.is_valid(raise_exception=True)
            user = serializerUser.save()

            serializerEmail = EmailVerificationUserSerializer(data={"user": user.id, "code": code})
            serializerEmail.is_valid(raise_exception=True)
            serializerEmail.save()

            send_email_register.delay(user.id)
            # transaction.on_commit(lambda: send_email_register.delay(user.id))

            refresh = RefreshToken.for_user(user)

            data = {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }

            return Response(data=data, status=status.HTTP_201_CREATED)
    
    @api_view(['POST'])
    def code(self, request):
        user = self.request.user

        if user is None:
            raise ValidationError("User not found!")
        
        if user.is_active:
            return Response(data={"error_code": "USER_ALREADY_ACTIVE", "message": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_email = EmailVerificationUser.objects.get(user=user.id)
        now_timestamp = datetime.datetime.now().timestamp()

        if now_timestamp - user_email.date_time >= 600:
            user_email.code = random.randint(100000, 999999)

            send_email_register.delay(user_email.user.id)

            return Response(data={"error_code": "TOKEN_EXPIRED", "message": "This token is expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user_email.code != request.data['code']:
            return Response(data={"error_code": "TOKEN_INVALID", "message": "The token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_active = True

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
        request.data['file'] = file

        serializer = UpdateUserSerializer(instance=user, data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)