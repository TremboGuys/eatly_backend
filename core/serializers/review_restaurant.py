from rest_framework.serializers import ModelSerializer, SerializerMethodField, HiddenField, CurrentUserDefault

from core.models import ReviewRestaurant, ResponseReviewRestaurant

from utils.helpers import verify_group_user

class ResponseReviewRestaurantSerializer(ModelSerializer):
    author_info = SerializerMethodField()
    author = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = ResponseReviewRestaurant
        fields = "__all__"
    
    def get_author_info(self, obj):
        author = {"id": obj.author.id}

        if hasattr(obj.author, "person"):
            author['type'] = "client"
            author['name'] = obj.author.person.name
        else:
            author['type'] = "restaurant"
            author['name'] = obj.author.restaurant.name
        
        return author
    
class ReviewRestaurantSerializer(ModelSerializer):
    response = SerializerMethodField()
    client = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = ReviewRestaurant
        fields = "__all__"
    
    def get_response(self, obj):
        return ResponseReviewRestaurantSerializer(obj.responses.all(), many=True).data
