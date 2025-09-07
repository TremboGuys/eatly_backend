from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction

from core.serializers import UserRegisterSerializer, TelephoneSerializer
from utils.helpers import relate_user_group

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        with transaction.atomic():
            serializerUser = UserRegisterSerializer(data=request.data['user'])
            serializerUser.is_valid(raise_exception=True)
            user = serializerUser.save()

            relate_user_group(request.data, user.id)

            request.data['telephone']['user'] = user.id

            serializerTel = TelephoneSerializer(data=request.data['telephone'])
            serializerTel.is_valid(raise_exception=True)
            serializerTel.save()

            return Response({"message": "User created with success", "userId": user.id}, status=status.HTTP_201_CREATED)