from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from core.models import Telephone
from core.serializers import CreateTelephoneSerializer, TelephoneSerializer

class TelephoneViewSet(ModelViewSet):
    queryset = Telephone.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTelephoneSerializer
        return TelephoneSerializer

    @action(detail=False, methods=['patch'], url_path="me")
    def update_me(self, request):
        instance = Telephone.objects.get(user=self.request.user.id)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)