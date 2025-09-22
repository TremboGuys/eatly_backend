from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, HiddenField, CurrentUserDefault, IntegerField

from core.models import Restaurant, RecentlyViews, ReviewRestaurant
from core.serializers import CategorySerializer, ProductCategorySerializer

class RestaurantSerializer(ModelSerializer):
    categories = ProductCategorySerializer(many=True)
    class Meta:
        model = Restaurant
        fields = "__all__"

class ListRestaurantSerializer(ModelSerializer):
    photo = SerializerMethodField()
    total_reviews = IntegerField(read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'note', 'average_delivery_time', 'photo', 'total_reviews']
    
    def get_photo(self, obj):
        return obj.user.photo

class RetrieveRestaurantSerializer(ModelSerializer):
    photo = SerializerMethodField()
    products = SerializerMethodField()
    categories = CategorySerializer(many=True)
    total_reviews = IntegerField(read_only=True)
    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_products(self, obj):
        from core.serializers import ListProductSerializer
        return ListProductSerializer(obj.user.products.all(), many=True).data
    
    def get_photo(self, obj):
        return obj.user.photo

class CreateRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"

class RecentlyViewsSerializer(ModelSerializer):
    client = HiddenField(default=CurrentUserDefault())
    restaurant_data = SerializerMethodField()

    class Meta:
        model = RecentlyViews
        fields = "__all__"
    
    def get_restaurant_data(self, obj):
        serializer = ListRestaurantSerializer(obj.restaurant)
        return serializer.data

class ListRecentlyViewsSerializer(ModelSerializer):
    restaurant_data = SerializerMethodField()

    class Meta:
        model = RecentlyViews
        fields = ["id", "restaurant_data"]

    def get_restaurant_data(self, obj):
        serializer = ListRestaurantSerializer(obj.restaurant)
        return serializer.data