from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Tours, Account, TourBooking, Payment
from .serializers import TourSerializer, AccountSerializer, TourBookingSerializer, PaymentSerializer
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema


class AccountViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.CreateAPIView,
                     generics.RetrieveAPIView,
                     generics.UpdateAPIView):
    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer
    parser_classes = [MultiPartParser, ]
    swagger_schema = None

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tours.objects.filter(active=True)
    serializer_class = TourSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Add tags to a tour',
        responses={
            status.HTTP_200_OK: TourSerializer()
        }
    )
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

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


class TourBookingViewSet(viewsets.ModelViewSet):
    queryset = TourBooking.objects.all()
    serializer_class = TourBookingSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


def index(request):
    return render(request, template_name='index.html', context={'name': 'Tuu'})
