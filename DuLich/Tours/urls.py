from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tours', views.TourViewSet)
router.register('users', views.AccountViewSet)
router.register('category', views.CategoryViewSet)
router.register('province', views.ProvinceViewSet)
router.register('blog', views.BlogViewSet)
router.register('payments', views.PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]