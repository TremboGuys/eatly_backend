from rest_framework.viewsets import ModelViewSet

from core.models import Product
from core.serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer