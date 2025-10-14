from itertools import groupby
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
    total_reviews = IntegerField(read_only=True)
    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_products(self, obj):
        from core.serializers import ListProductSerializer

        products = obj.user.products.prefetch_related("categories").all()

        result = []
        groups = {}

        for product in products:
            for category in product.categories.all():
                if category.name not in groups:
                    groups[category.name] = []
                groups[category.name].append({
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "is_adult": product.is_adult,
                    "url_file": product.url_file,
                })
        
        for category, products in groups.items():
            result.append({
                "category": category,
                "products": products
            })
        
        return result
    
    def get_photo(self, obj):
        return obj.user.photo
    
    # Fazer um def get_categories com um set para categories

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