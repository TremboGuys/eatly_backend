from rest_framework.serializers import ModelSerializer, SerializerMethodField, HiddenField, CurrentUserDefault, ValidationError
from django.db import transaction

from core.models import ReviewDeliveryman, ResponseReviewDeliveryman, NaturalPerson, Order

class ResponseReviewDeliverymanSerializer(ModelSerializer):
    author = HiddenField(default=CurrentUserDefault())
    author_info = SerializerMethodField()
    class Meta:
        model = ResponseReviewDeliveryman
        fields = "__all__"
    
    def get_author_info(self, obj):
        author_info = {"id": obj.author.id, "name": obj.author.person.name}

        if obj.author.groups.filter(name="client").exists():
            author_info['type'] = "client"
        else:
            author_info['type'] = "deliveryman"
        
        return author_info

class UpdateResponseReviewDeliverymanSerializer(ModelSerializer):
    class Meta:
        model = ResponseReviewDeliveryman
        fields = ['comment']

class ReviewDeliverymanSerializer(ModelSerializer):
    responses = SerializerMethodField()
    client = HiddenField(default=CurrentUserDefault())
    client_info = SerializerMethodField()
    class Meta:
        model = ReviewDeliveryman
        fields = "__all__"
    
    def get_client_info(self, obj):
        client_info = {"name": obj.client.person.name}

        return client_info
    
    def get_responses(self, obj):
        return ResponseReviewDeliverymanSerializer(obj.responses.all(), many=True).data
    
    def create(self, validated_data):
        with transaction.atomic():
            review = super().create(validated_data)
            deliveryman = NaturalPerson.objects.get(id=review.deliveryman.person.id)
            quantity_review = ReviewDeliveryman.objects.filter(deliveryman=deliveryman.id).count()
            if quantity_review == 0:
                note_deliveryman = review.note
            else:
                note_deliveryman = ((deliveryman.note * (quantity_review - 1)) + review.note) / quantity_review
            deliveryman.note = "{:.1f}".format(note_deliveryman)

            deliveryman.save()

            return review
    
    def validate(self, attrs):
        if attrs.get('order') != None:
            order = attrs.get('order')
            if order.client != self.context['request'].user:
                raise ValidationError({"error": "This order was not placed by this client"})
            if order.deliveryman == None or order.deliveryman != attrs['deliveryman']:
                raise ValidationError({"error": "This Order was not delivered by this deliveryman!"})
        
        return attrs

class UpdateReviewDeliverymanSerializer(ModelSerializer):
    class Meta:
        model = ReviewDeliveryman
        fields = ['comment', 'note']
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            old_note = instance.note
            new_note = validated_data.get('note', old_note)
            print(old_note, new_note)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if new_note != old_note:
                deliveryman = NaturalPerson.objects.get(id=instance.deliveryman.person.id)
                n = ReviewDeliveryman.objects.filter(deliveryman=instance.deliveryman).count()
                print(n)
                current_avg = float(deliveryman.note)
                new_avg = (current_avg * n - float(old_note) + float(new_note)) / n
                deliveryman.note = new_avg
                print(deliveryman.note)
                deliveryman.save()

        return instance