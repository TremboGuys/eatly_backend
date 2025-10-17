from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

from usuario.models import Usuario
from core.serializers import UserRegisterSerializer, TelephoneSerializer, ListUserSerializer, UpdateUserSerializer
from utils.helpers import relate_user_group, create_image, update_image

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        with transaction.atomic():
            data = request.data.copy()
            data['file'] = request.FILES.get("file", None)
            serializerUser = UserRegisterSerializer(data=data)
            serializerUser.is_valid(raise_exception=True)
            user = serializerUser.save()
            user.is_active = True
            user.save()

            refresh = RefreshToken.for_user(user)

            data = {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
                
            # relate_user_group(request.data, user.id)

            return Response(data=data, status=status.HTTP_201_CREATED)

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