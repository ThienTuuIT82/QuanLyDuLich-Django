from datetime import date
from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.utils import timezone


class Role(Enum):
    ADMIN = 'Admin'
    EMPLOYEE = 'Employee'
    USER = 'User'


class Gender(Enum):
    MALE = 'Nam'
    FEMALE = 'Nữ'


class Methods(Enum):
    ZALOPAY = 'ZaloPay'
    MOMO = 'Momo'
    CASH = 'Cash'


class Rate(Enum):
    LIKE = 'Like'
    DISLIKE = 'Dislike'


class Status(Enum):
    ACTIVE = 'Active'
    CANCELLED = 'Cancelled'
    ARCHIVED = 'Archived'


class Account(AbstractUser):
    class Meta:
        unique_together: {'username', 'role'}
    gender = models.CharField(max_length=20, choices=[(g.name, g.value) for g in Gender], default=Gender.MALE.value, null=True)
    birth = models.DateField(null=False, default=timezone.now())
    phone = models.CharField(max_length=12, null=True, blank=True)
    role = models.CharField(max_length=20, choices=[(r.name, r.value) for r in Role], default=Role.USER.value)
    avatar = models.ImageField(upload_to='upload/avatars/%Y/%m', null=True, blank=True)
    street = models.CharField(max_length=45, null=True, blank=True)
    city = models.CharField(max_length=45, null=True, blank=True)
    about = models.CharField(max_length=45, null=True, blank=True)


class Category(models.Model):
    class Meta:
        unique_together = ('name',)

    name = models.CharField(max_length=100, null=False, unique=True)


class Tours(models.Model):
    class Meta:
        unique_together = ('name',)
    name = models.CharField(max_length=100, null=False, unique=True)
    description = RichTextField()
    start_date = models.DateField(null=False)
    finish_date = models.DateField(null=False)
    destination = models.CharField(max_length=255, null=False)
    photos = models.ImageField(upload_to='upload/tours/%Y/%m', default=None)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category', related_query_name='my_category')
    tags = models.ManyToManyField('Tag', related_name='tags', related_query_name='my_tags')


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name


class Payment(models.Model):
    date = models.DateField(null=False)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    description = RichTextField()
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='user_payment', related_query_name='user_payment')
    method = models.CharField(max_length=20, choices=[(m.name, m.value) for m in Methods], default=Methods.CASH.value, null=True)
    tour = models.ForeignKey(Tours, on_delete=models.SET_NULL, null=True, related_name='tour_payment', related_query_name='tour_payment')


class TourBooking(models.Model):
    date = models.DateField(null=False)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='user_tourbooking', related_query_name='user_tourbooking')
    status = models.CharField(max_length=20, choices=[(s.name, s.value) for s in Status], default=Status.ACTIVE.value, null=True)
    tour = models.ForeignKey(Tours, on_delete=models.SET_NULL, null=True, related_name='tourbooking_payment', related_query_name='tourbooking_payment')


class RateTour(models.Model):
    rate = models.CharField(max_length=20, choices=[(r.name, r.value) for r in Rate])
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='my_user_ratetour', related_query_name='my_user_ratetour')
    tour = models.ForeignKey(Tours, on_delete=models.SET_NULL, null=True, related_name='rate_payment', related_query_name='rate_payment')


class CommentTour(models.Model):
    comment = models.TextField()
    photo = models.FileField(upload_to='upload/comment/%Y/%m', null=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='my_user_commenttour', related_query_name='my_user_commenttour')
    tour = models.ForeignKey(Tours, on_delete=models.SET_NULL, null=True, related_name='comment_payment', related_query_name='comment_payment')