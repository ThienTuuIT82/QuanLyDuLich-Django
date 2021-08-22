from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tours', views.TourViewSet)
router.register('users', views.AccountViewSet)
router.register('tourbooking', views.TourBookingViewSet)
router.register('payments', views.PaymentViewSet)
router.register('ratetour', views.RateTourViewSet)
router.register('commenttour', views.CommentTourViewSet)

urlpatterns = [
    path('', include(router.urls)),
]