from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Tours, Tag, Account, Payment, RateTour, CommentTour, Category, RateBlog, CommentBlog, \
    Blog, Province, TourView


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
    creator = SerializerMethodField()

    def get_creator(self, comment):
        return AccountSerializer(comment.creator, context={"request": self.context.get('request')}).data

    class Meta:
        model = CommentTour
        fields = ["id", "content", "tour", 'created_date', 'updated_date', 'creator']


class TourSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Tours
        fields = ["id", "name", "description", "start_date", "finish_date", "destination", "photos", "price_adult", "price_children", "active", "category", "tags", "vehicle"]


class TourDetailSerializer(TourSerializer):
    rate = SerializerMethodField()

    def get_rate(self, lesson):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            r = lesson.ratetour_set.filter(user=request.user).first()
            if r:
                return r.rate

        return -1

    class Meta:
        model = TourSerializer.Meta.model
        fields = TourSerializer.Meta.fields + ["rate"]


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "created_date", "price", "adult", "children", "status", "description", "user", "tour", "method"]


class RateTourSerializer(ModelSerializer):
    class Meta:
        model = RateTour
        fields = ["id", "rate", "user", "tour", "created_date"]


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


class TourViewSerializer(ModelSerializer):
    class Meta:
        model = TourView
        fields = ["id", "views", "tour"]