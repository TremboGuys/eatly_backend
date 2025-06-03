from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.serializers import UserRegisterSerializer

class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({"message": "User created with success", "userId": user.id}, status=status.HTTP_201_CREATED)