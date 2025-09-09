from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from core.models import ReviewDeliveryman, ResponseReviewDeliveryman, NaturalPerson
from core.serializers import ReviewDeliverymanSerializer, UpdateReviewDeliverymanSerializer, ResponseReviewDeliverymanSerializer, UpdateResponseReviewDeliverymanSerializer

class ReviewDeliverymanViewSet(ModelViewSet):
    queryset = ReviewDeliveryman.objects.all()

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UpdateReviewDeliverymanSerializer
        else:
            return ReviewDeliverymanSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = ReviewDeliveryman.objects.get(id=instance.id)

        print(instance.deliveryman.id)

        deliveryman = NaturalPerson.objects.get(user=instance.deliveryman.id)
        quantity_reviews = ReviewDeliveryman.objects.filter(deliveryman=deliveryman.id).count()
        if quantity_reviews == 1:
            note_deliveryman = 5.0
        else:
            note_deliveryman = ((deliveryman.note * quantity_reviews) - instance.note) / (quantity_reviews - 1)
        deliveryman.note = note_deliveryman
        deliveryman.save()

        instance.delete()

        return Response({"message": "Review of deliveryman deleted with success!"}, status=status.HTTP_204_NO_CONTENT)

class ResponseReviewDeliverymanViewSet(ModelViewSet):
    queryset = ResponseReviewDeliveryman.objects.all()

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UpdateResponseReviewDeliverymanSerializer
        else:
            return ResponseReviewDeliverymanSerializer 