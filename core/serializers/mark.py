from rest_framework.serializers import ModelSerializer

from core.models import Mark

class MarkSerializer(ModelSerializer):
    class Meta:
        model = Mark
        fields = "__all__"