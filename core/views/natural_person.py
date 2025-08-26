from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import NaturalPerson
from core.serializers import NaturalPersonSerializer

class NaturalPersonViewSet(ModelViewSet):
    queryset = NaturalPerson.objects.all()
    serializer_class = NaturalPersonSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response({"message": "Natural Person created with success", "data": response.data}, status=status.HTTP_201_CREATED)