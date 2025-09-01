from rest_framework.viewsets import ModelViewSet

from core.models import Coupon, CouponClient, CouponClientOrder
from core.serializers import CouponSerializer, CouponClientSerializer, CouponClientOrderSerializer

class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class CouponClientViewSet(ModelViewSet):
    queryset = CouponClient.objects.all()
    serializer_class = CouponClientSerializer

class CouponClientOrderViewSet(ModelViewSet):
    queryset = CouponClientOrder.objects.all()
    serializer_class = CouponClientOrderSerializer