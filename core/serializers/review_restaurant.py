from rest_framework.serializers import ModelSerializer, SerializerMethodField, HiddenField, CurrentUserDefault, ValidationError
from django.db import transaction

from core.models import ReviewRestaurant, ResponseReviewRestaurant, Restaurant

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

class UpdateResponseReviewRestaurantSerializer(ModelSerializer):
    class Meta:
        model = ResponseReviewRestaurant
        fields = ['comment']
    
class ReviewRestaurantSerializer(ModelSerializer):
    response = SerializerMethodField()
    client = HiddenField(default=CurrentUserDefault())
    client_info = SerializerMethodField()
    class Meta:
        model = ReviewRestaurant
        fields = "__all__"
    
    def get_response(self, obj):
        return ResponseReviewRestaurantSerializer(obj.responses.all(), many=True).data
    
    def get_client_info(self, obj):
        client_info = {"name": obj.client.person.name}
        
        return client_info
    
    def create(self, validated_data):
        with transaction.atomic():
            review = super().create(validated_data)
            restaurant = Restaurant.objects.get(id=review.restaurant.id)
            quantity_review = ReviewRestaurant.objects.filter(restaurant=restaurant.id).count()
            if quantity_review == 0:
                note_restaurant = review.note
            else:
                note_restaurant = ((restaurant.note * (quantity_review - 1)) + review.note) / quantity_review
            restaurant.note = "{:.1f}".format(note_restaurant)

            restaurant.save()

            return review
    
    def validate(self, attrs):
        if hasattr(attrs, "order"):
            if attrs['order'].client != self.context['request'].user:
                raise ValidationError({"error": "This order was not placed by this client"})
            if attrs['order'].restaurant != attrs['restaurant']:
                raise ValidationError({"error": "This Order was not placed by this restaurant!"})
        
        return attrs

class UpdateReviewRestaurantSerializer(ModelSerializer):
    class Meta:
        model = ReviewRestaurant
        fields = ['comment', 'note']

    def update(self, instance, validated_data):
        with transaction.atomic():
            old_note = instance.note
            new_note = validated_data.get('note', old_note)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if new_note != old_note:
                restaurant = instance.restaurant
                n = ReviewRestaurant.objects.filter(restaurant=restaurant).count()
                current_avg = float(restaurant.note)
                new_avg = (current_avg * n - float(old_note) + float(new_note)) / n
                restaurant.note = "{:.1f}".format(new_avg)
                restaurant.save()

        return instance