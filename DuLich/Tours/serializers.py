from rest_framework.serializers import ModelSerializer
from .models import Tours, Tag, Account, Payment, TourBooking, RateTour, CommentTour, Category, RateBlog, CommentBlog, \
    Blog, Province


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name", "email", "username", "password", "avatar", "gender", "phone", "birth", "role", "street", "province", "about"]
        extra_kwags = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        account = Account(**validated_data)
        account.set_password(validated_data['password'])
        account.save()

        return account


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class CommentTourSerializer(ModelSerializer):
    class Meta:
        model = CommentTour
        fields = ["id", "content", "user", "tour", 'created_date', 'updated_date']


class TourSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    comment = CommentTourSerializer(many=True)
    class Meta:
        model = Tours
        fields = ["id", "name", "description", "start_date", "finish_date", "destination", "photos", "price", "active", "category", "tags", "vehicle", "comment"]


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "created_date", "price", "description", "user", "tour", "method"]


class TourBookingSerializer(ModelSerializer):
    class Meta:
        model = TourBooking
        fields = ["id", "created_date", "price", "user", "status"]


class RateTourSerializer(ModelSerializer):
    class Meta:
        model = RateTour
        fields = ["id", "rate", "user", "tour"]


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "name", "photo", "created_date", "user", "description"]


class RateBlogSerializer(ModelSerializer):
    class Meta:
        model = RateBlog
        fields = ["id", "rate", "user", "blog"]


class CommentBlogSerializer(ModelSerializer):
    class Meta:
        model = CommentBlog
        fields = ["id", "comment", "user", "blog", 'created_date', 'updated_date']


class ProvinceSerializer(ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name"]