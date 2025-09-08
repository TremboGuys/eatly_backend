from rest_framework.serializers import ModelSerializer, SerializerMethodField, HiddenField, CurrentUserDefault
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
        review = super().create(validated_data)
        restaurant = Restaurant.objects.get(id=review.restaurant.id)
        quantity_review = ReviewRestaurant.objects.filter(restaurant=restaurant.id).count()
        note_restaurant = ((restaurant.note * (quantity_review - 1)) + review.note) / quantity_review
        restaurant.note = "{:.1f}".format(note_restaurant)

        restaurant.save()

        return review
    
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