from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, filters
from django.db.models import Count, F, ExpressionWrapper, FloatField
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Restaurant, RecentlyViews
from core.serializers import RestaurantSerializer, CreateRestaurantSerializer, RetrieveRestaurantSerializer, ListRestaurantSerializer, RecentlyViewsSerializer, ListRecentlyViewsSerializer

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all().annotate(total_reviews=Count("reviews"))
    
    def list(self, request, *args, **kwargs):
        page = request.GET.get("page", 1)
        weight_params_map = {
            "total_reviews": 0.5,
            "note": 0.4,
            "average_delivery_time": 0.1
        }

        expression = None

        for key, value in request.GET.items():
            if key == "search" or key == "page":
                continue
            if value == "bigger":
                part = F(key) * weight_params_map[key]
            else:
                part = F(key) * -weight_params_map[key]
            
            expression = part if expression is None else expression + part
            
            if key == "note":
                expression = ExpressionWrapper(expression, output_field=FloatField()) + ExpressionWrapper(F("total_reviews") * weight_params_map["total_reviews"], output_field=FloatField())

        if expression is not None:
            restaurant = self.filter_queryset(self.queryset)

            restaurant = restaurant.annotate(total_reviews=Count("reviews"), priority=ExpressionWrapper(expression=expression, output_field=FloatField())).order_by("-priority")
        else:
            restaurant = Restaurant.objects.annotate(total_reviews=Count("reviews")).order_by("-total_reviews")

            restaurant = self.filter_queryset(self.queryset)

        restaurants_per_query = Paginator(restaurant, 10)
        serializer = ListRestaurantSerializer(restaurants_per_query.get_page(page), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateRestaurantSerializer
        if self.action == "retrieve":
            return RetrieveRestaurantSerializer
        if self.action == "list":
            return ListRestaurantSerializer
        return RestaurantSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class RecentlyViewsViewSet(ModelViewSet):
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return RecentlyViews.objects.all()
        else:
            return RecentlyViews.objects.filter(client=user.id).order_by("viewed_at")
    
    def get_serializer_class(self):
        if self.action == "list":
            return ListRecentlyViewsSerializer
        else:
            return RecentlyViewsSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        query = RecentlyViews.objects.filter(client=user.id).order_by("-viewed_at")
        paginator = Paginator(query, 15)
        serializer = ListRecentlyViewsSerializer(paginator.get_page(1), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        if (self.get_queryset().count() == 20):
            self.get_queryset().last().delete()
            RecentlyViews.save()
        return super().create(request, *args, **kwargs)