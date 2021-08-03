from rest_framework.serializers import ModelSerializer
from .models import Tours


class TourSerializer(ModelSerializer):
    class Meta:
        model = Tours
        fields = ["id", "name", "start_date", "finish_date", "destination", "photos", "price", "active", "category"]