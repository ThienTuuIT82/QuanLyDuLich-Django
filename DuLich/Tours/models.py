from datetime import date
from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.utils import timezone


class Role(Enum):
    ADMIN = 'Admin'
    BUSINESS = 'Nhân viên kinh doanh'
    SALESMAN = 'Nhân viên bán hàng'
    USER = 'Khách hàng'


class Gender(Enum):
    MALE = 'Nam'
    FEMALE = 'Nữ'


class Methods(Enum):
    ZALOPAY = 'ZaloPay'
    MOMO = 'Momo'
    TRANSFER = 'Chuyển khoản'


class StatusPayment(Enum):
    PAID = 'Đã thanh toán'
    UNPAID = 'Chưa thanh toán'
    EXPIRED = 'Đã hết hạn'


class Vehicle(Enum):
    OTO = 'Ô tô'
    YACHT = 'Du thuyền'
    PLANE = 'Máy bay'


class Province(models.Model):
    name = models.CharField(max_length=20, null=True, unique=True)


class Account(AbstractUser):
    class Meta:
        unique_together: {'username', 'email'}

    gender = models.CharField(max_length=20, choices=[(g.name, g.value) for g in Gender], default=Gender.MALE,
                              null=True)
    birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    role = models.CharField(max_length=20, choices=[(r.name, r.value) for r in Role], default=Role.USER)
    avatar = models.ImageField(upload_to='static/upload/avatars/%Y/%m', null=True, blank=True)
    street = models.CharField(max_length=45, null=True, blank=True)
    about = models.CharField(max_length=45, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, related_name='province',
                                 related_query_name='province')


class Category(models.Model):
    class Meta:
        unique_together = ('name',)

    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class Tours(models.Model):
    class Meta:
        unique_together = ('name',)

    name = models.CharField(max_length=100, null=False, unique=True)
    description = RichTextField()
    start_date = models.DateField(null=False)
    finish_date = models.DateField(null=False)
    destination = models.CharField(max_length=255, null=False)
    photos = models.ImageField(upload_to='static/upload/tours/%Y/%m', default=None)
    price_adult = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    price_children = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    vehicle = models.CharField(max_length=20, choices=[(v.name, v.value) for v in Vehicle], default=Vehicle.OTO)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category',
                                 related_query_name='my_category')
    tags = models.ManyToManyField('Tag', related_name='tags', related_query_name='my_tags')
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='user_tour',
                             related_query_name='user_tour')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name


class Payment(models.Model):
    created_date = models.DateField(null=False, auto_created=True)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    description = RichTextField()
    adult = models.IntegerField(null=False, default=1)
    children = models.IntegerField(null=False, default=0)
    status = models.CharField(max_length=20, choices=[(r.name, r.value) for r in StatusPayment], default=StatusPayment.UNPAID)

    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='user_payment',
                             related_query_name='user_payment')
    method = models.CharField(max_length=20, choices=[(m.name, m.value) for m in Methods], default=Methods.TRANSFER.value,
                              null=True)
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True, related_name='tour_payment',
                             related_query_name='tour_payment')


class RateTour(models.Model):
    rate = models.PositiveSmallIntegerField(default=0)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(null=True, auto_now=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ['tour', 'user']


class CommentTour(models.Model):
    content = RichTextField()
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    photo = models.FileField(upload_to='static/upload/comment/%Y/%m', null=True)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.content


class TourView(models.Model):
    views = models.IntegerField(default=0)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(null=True, auto_now=True)
    tour = models.OneToOneField(Tours, on_delete=models.CASCADE)


class Blog(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)
    photo = models.FileField(upload_to='static/upload/blog/%Y/%m', null=True)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(null=True, auto_now=True)
    description = RichTextField()
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='my_user_blog',
                             related_query_name='my_user_blog')


class RateBlog(models.Model):
    rate = models.PositiveSmallIntegerField(default=0)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(null=True, auto_now=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ['blog', 'user']


class CommentBlog(models.Model):
    content = RichTextField(default="")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    photo = models.FileField(upload_to='static/upload/comment/%Y/%m', null=True)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.content