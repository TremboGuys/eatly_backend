from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction

from core.serializers import UserRegisterSerializer, NaturalPersonSerializer, TelephoneSerializer

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        with transaction.atomic():
            npModel = {"name": request.data.pop('name'), "date_birth": request.data.pop('date_birth')}
            cellphoneModel = {"telephone_type": 1, "number_e164": request.data.pop('cellphone'), "is_principal": True}
            serializerUser = UserRegisterSerializer(data=request.data)
            serializerUser.is_valid(raise_exception=True)
            user = serializerUser.save()

            npModel['user'] = user.id

            serializerNP = NaturalPersonSerializer(data=npModel)
            serializerNP.is_valid(raise_exception=True)
            serializerNP.save()

            serializerTel = TelephoneSerializer(data=cellphoneModel)
            serializerTel.is_valid(raise_exception=True)
            serializerTel.save()

            return Response({"message": "User created with success", "userId": user.id}, status=status.HTTP_201_CREATED)