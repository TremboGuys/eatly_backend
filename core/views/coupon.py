from rest_framework.viewsets import ModelViewSet

from core.models import Coupon, CouponClient, CouponClientOrder
from core.serializers import CouponSerializer, CouponClientSerializer, CouponClientOrderSerializer

class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class CouponClientViewSet(ModelViewSet):
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return CouponClient.objects.all()
        return CouponClient.objects.filter(client=user)
    
    serializer_class = CouponClientSerializer

class CouponClientOrderViewSet(ModelViewSet):
    queryset = CouponClientOrder.objects.all()
    serializer_class = CouponClientOrderSerializer