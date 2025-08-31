import json
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.models import Category
from core.serializers import CategorySerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES['file']
        request.data['file'] = file

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Category created with sucess", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response({"message: Category does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        file = request.FILES['file']
        request.data['file'] = file
        
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message: Category updated with success"}, serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)