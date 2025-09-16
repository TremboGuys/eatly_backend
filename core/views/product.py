from rest_framework.viewsets import ModelViewSet

from core.models import Product
from core.serializers import ProductSerializer, ListProductSerializer, RetrieveProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ListProductSerializer
        elif self.action == "retrieve":
            return RetrieveProductSerializer
        else:
            return ProductSerializer