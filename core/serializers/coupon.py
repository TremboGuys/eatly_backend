from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from core.models import Coupon, CouponClient, CouponClientOrder

class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

class CouponClientSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = CouponClient
        fields = "__all__"

class CouponClientOrderSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = CouponClientOrder
        fields = "__all__"