from rest_framework.serializers import ModelSerializer
from .models import Tours, Tag, Account, Payment, TourBooking, RateTour, CommentTour


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name", "email", "username", "password", "avatar", "gender", "phone", "birth", "role", "street", "city", "about"]
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
        fields = ["id", "name", "description", "start_date", "finish_date", "destination", "photos", "price", "active", "category", "tags"]


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "date", "price", "description", "user", "tour", "method"]


class TourBookingSerializer(ModelSerializer):
    class Meta:
        model = TourBooking
        fields = ["id", "date", "price", "user", "status"]


class RateTourSerializer(ModelSerializer):
    class Meta:
        model = RateTour
        fields = ["id", "rate", "user", "tour"]


class CommentTourSerializer(ModelSerializer):
    class Meta:
        model = CommentTour
        fields = ["id", "comment", "photo", "user", "tour"]
