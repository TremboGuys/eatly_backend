from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Product
from core.serializers import ProductSerializer, ListProductSerializer, RetrieveProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filters_fields = ['restaurant']

    def get_serializer_class(self):
        if self.action == "list":
            return ListProductSerializer
        elif self.action == "retrieve":
            return RetrieveProductSerializer
        else:
            return ProductSerializer