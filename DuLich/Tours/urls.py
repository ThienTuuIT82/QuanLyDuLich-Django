from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tours', views.TourViewSet)
router.register('users', views.AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
]