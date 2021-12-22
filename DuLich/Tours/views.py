from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from .models import Tours, Account, Payment, RateTour, CommentTour, Category, Tag, Province, Blog, \
    TourView, CommentBlog, RateBlog
from .serializers import TourSerializer, AccountSerializer, PaymentSerializer, \
    RateTourSerializer, CommentTourSerializer, CategorySerializer, ProvinceSerializer, BlogSerializer, \
    TourViewSerializer, TourDetailSerializer, CommentBlogSerializer, RateBlogSerializer, BlogDetailSerializer
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.http import Http404
from django.db.models import F


class AccountViewSet(viewsets.ViewSet,
                     generics.CreateAPIView,
                     generics.UpdateAPIView):
    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={"request": request}).data,
                        status=status.HTTP_200_OK)


class ProvinceViewSet(viewsets.ViewSet,
                  generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class ToursPagination(PageNumberPagination):
    page_size = 9


class TourViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.RetrieveAPIView):
    queryset = Tours.objects.filter(active=True)
    serializer_class = TourDetailSerializer
    pagination_class = ToursPagination

    @swagger_auto_schema(
        operation_description='Add tags to a tour',
        responses={
            status.HTTP_200_OK: TourSerializer()
        }
    )
    def get_permissions(self):
        if self.action in ['add_comment', 'rate']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get_queryset(self):
        tours = Tours.objects.filter(active=True)

        q = self.request.query_params.get('q')
        if q is not None:
            tours = tours.filter(name__icontains=q)

        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            tours = tours.filter(category_id=cate_id)

        return tours

    @action(methods=['post'], detail=True, url_path='hide-tour', url_name='hide-tour')
    def hide_tour(self, request, pk):
        try:
            t = Tours.objects.get(pk=pk)
            t.active = False
            t.save()
        except Tours.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=TourSerializer(t, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='tags')
    def add_tag(self, request, pk):
        try:
            tour = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get('tags')
            if tags is not None:
                for tag in tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    tour.tags.add(t)

                tour.save()
                return Response(self.serializer_class(tour).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        content = request.data.get('content')
        photo = request.data.get('photo')
        if content:
            c = CommentTour.objects.create(content=content,
                                           photo=photo,
                                           tour=self.get_object(),
                                           creator=request.user)

            return Response(CommentTourSerializer(c).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='rating')
    def rate(self, request, pk):
        try:
            rate = int(request.data['rating'])
        except IndexError or ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = RateTour.objects.update_or_create(user=request.user,
                                                  tour=self.get_object(),
                                                  defaults={"rate": rate})

            return Response(RateTourSerializer(r).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='views')
    def inc_view(self, request, pk):
        v, created = TourView.objects.get_or_create(tour=self.get_object())
        v.views = F('views') + 1
        v.save()

        v.refresh_from_db()

        return Response(TourViewSerializer(v).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="comments")
    def get_comments(self, request, pk):
        c = self.get_object()
        return Response(
            CommentTourSerializer(c.commenttour_set.order_by("-id").all(), many=True, context={"request": self.request}).data,
            status=status.HTTP_200_OK)


class BlogViewSet(viewsets.ModelViewSet,
                  generics.ListAPIView,
                  generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer

    def get_permissions(self):
        if self.action in ['add_comment', 'rate']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='add-comment-blog')
    def add_comment(self, request, pk):
        content = request.data.get('content')
        photo = request.data.get('photo')
        if content:
            c = CommentBlog.objects.create(content=content,
                                           photo=photo,
                                           blog=self.get_object(),
                                           creator=request.user)

            return Response(CommentBlogSerializer(c).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='rating-blog')
    def rate(self, request, pk):
        try:
            rate = int(request.data['rating'])
        except IndexError or ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = RateBlog.objects.update_or_create(user=request.user,
                                                  blog=self.get_object(),
                                                  defaults={"rate": rate})

            return Response(RateBlogSerializer(r).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="comments-blog")
    def get_comments(self, request, pk):
        c = self.get_object()
        return Response(
            CommentBlogSerializer(c.commentblog_set.order_by("-id").all(), many=True,
                                  context={"request": self.request}).data,
            status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.action == 'add_payment':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='add-payment')
    def add_payment(self, request, pk):
        user_id = request.data.get('userId')
        tour_id = request.data.get('tourId')
        method = request.data.get('method')
        adult = request.data.get('adult')
        children = request.data.get('children')
        price = request.data.get('price')
        res = Payment.objects.create(tour=tour_id,
                                      user=user_id,
                                      method=method,
                                      adult=adult,
                                      children=children,
                                      price=price)
        return Response(PaymentSerializer(res).data, status=status.HTTP_201_CREATED)


class RateTourViewSet(viewsets.ModelViewSet):
    queryset = RateTour.objects.all()
    serializer_class = RateTourSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class RateBlogViewSet(viewsets.ModelViewSet):
    queryset = RateBlog.objects.all()
    serializer_class = RateBlogSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class CommentTourViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CommentTour.objects.all()
    serializer_class = CommentTourSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentBlogViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CommentBlog.objects.all()
    serializer_class = CommentBlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


def index(request):
    return render(request, template_name='index.html', context={'name': 'Tuu'})


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)