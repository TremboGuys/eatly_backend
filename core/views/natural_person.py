from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from core.models import NaturalPerson
from core.serializers import CreateUpdateNaturalPersonSerializer, NaturalPersonSerializer

class NaturalPersonViewSet(ModelViewSet):
    queryset = NaturalPerson.objects.all()
    http_method_names = ['get', 'post', 'patch']
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUpdateNaturalPersonSerializer
        return NaturalPersonSerializer

    @action(detail=False, methods=['patch'], url_path='me')
    def update_me(self, request):
        instance = NaturalPerson.objects.get(user=self.request.user.id)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['PATCH'], url_path='me/google')
    def update_me_google(self, request):
        instance = NaturalPerson.objects.get(user=request.data.pop('user'))
        serializer = CreateUpdateNaturalPersonSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)