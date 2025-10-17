from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from core.models import NaturalPerson
from core.serializers import NaturalPersonSerializer

class NaturalPersonViewSet(ModelViewSet):
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonSerializer
    http_method_names = ['get', 'post', 'patch']
    permission_classes = [AllowAny]

    @action(detail=False, methods=['patch'], url_path='me')
    def update_me(self, request):
        instance = NaturalPerson.objects.get(user=self.request.user.id)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response({"message": "Natural Person created with success", "data": response.data}, status=status.HTTP_201_CREATED)