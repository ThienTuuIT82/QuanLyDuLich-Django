from rest_framework.serializers import ModelSerializer
from .models import Tours, Tag, Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name", "email", "username", "password", "avatar"]
        extra_kwags = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        account = Account(**validated_data)
        account.set_password(validated_data['password'])
        account.save()

        return account


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TourSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Tours
        fields = ["id", "name", "start_date", "finish_date", "destination", "photos", "price", "active", "category", "tags"]