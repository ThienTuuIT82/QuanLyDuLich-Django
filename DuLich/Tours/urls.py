from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tours', views.TourViewSet)
router.register('users', views.AccountViewSet)
router.register('category', views.CategoryViewSet)
router.register('tourbooking', views.TourBookingViewSet)
router.register('payments', views.PaymentViewSet)
router.register('ratetour', views.RateTourViewSet)
router.register('commenttour', views.CommentTourViewSet)
router.register('province', views.ProvinceViewSet)
router.register('blog', views.BlogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]