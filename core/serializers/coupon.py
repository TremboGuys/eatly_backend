from rest_framework.serializers import ModelSerializer

from core.models import Coupon, CouponClient, CouponClientOrder

class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

class CouponClientSerializer(ModelSerializer):
    class Meta:
        model = CouponClient
        fields = "__all__"

class CouponClientOrderSerializer(ModelSerializer):
    class Meta:
        model = CouponClientOrder
        fields = "__all__"