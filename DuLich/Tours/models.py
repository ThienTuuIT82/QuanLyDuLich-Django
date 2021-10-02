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
    EMPLOYEE_MANAGER = 'Quản lý nhân sự'
    MANAGER = 'Quản lý'
    USER = 'Khách hàng'


class Gender(Enum):
    MALE = 'Nam'
    FEMALE = 'Nữ'


class Methods(Enum):
    ZALOPAY = 'ZaloPay'
    MOMO = 'Momo'
    TRANSFER = 'Chuyển khoản'


class Rate(Enum):
    LIKE = 'Like'
    DISLIKE = 'Dislike'


class Status(Enum):
    ACTIVE = 'Active'
    CANCELLED = 'Cancelled'
    ARCHIVED = 'Archived'


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
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    vehicle = models.CharField(max_length=20, choices=[(v.name, v.value) for v in Vehicle], default=Vehicle.OTO)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category',
                                 related_query_name='my_category')
    tags = models.ManyToManyField('Tag', related_name='tags', related_query_name='my_tags')
    comment = models.ManyToManyField('CommentTour', related_name='comment', related_query_name='commenttour')
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
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='user_payment',
                             related_query_name='user_payment')
    method = models.CharField(max_length=20, choices=[(m.name, m.value) for m in Methods], default=Methods.TRANSFER.value,
                              null=True)
    tour = models.ForeignKey(Tours, on_delete=models.SET_NULL, null=True, related_name='tour_payment',
                             related_query_name='tour_payment')


class TourBooking(models.Model):
    created_date = models.DateField(null=False)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='user_tourbooking',
                             related_query_name='user_tourbooking')
    status = models.CharField(max_length=20, choices=[(s.name, s.value) for s in Status], default=Status.ACTIVE.value,
                              null=True)
    tour = models.ForeignKey(Tours, on_delete=models.SET_NULL, null=True, related_name='tourbooking_payment',
                             related_query_name='tourbooking_payment')


class RateTour(models.Model):
    rate = models.CharField(max_length=20, choices=[(r.name, r.value) for r in Rate])
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)


class CommentTour(models.Model):
    content = RichTextField()
    photo = models.FileField(upload_to='static/upload/comment/%Y/%m', null=True)
    created_date = models.DateField(null=True, auto_now_add=True)
    updated_date = models.DateField(null=True, auto_now=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content


class ReplyTour(models.Model):
    comment = models.TextField()
    photo = models.FileField(upload_to='static/upload/comment/%Y/%m', null=True)
    created_date = models.DateField(null=True, auto_now_add=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='my_user_reply_tour',
                             related_query_name='my_user_reply_tour')
    tour = models.ForeignKey(Tours, on_delete=models.SET_NULL, null=True, related_name='reply_payment',
                             related_query_name='reply_payment')
    comment_tour = models.ForeignKey(CommentTour, on_delete=models.CASCADE,
                                     related_name='comment_reply_tour')


class Blog(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)
    photo = models.FileField(upload_to='static/upload/blog/%Y/%m', null=True)
    created_date = models.DateField(null=True)
    description = RichTextField()
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='my_user_blog',
                             related_query_name='my_user_blog')


class RateBlog(models.Model):
    rate = models.CharField(max_length=20, choices=[(r.name, r.value) for r in Rate])
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='my_user_rateblog',
                             related_query_name='my_user_rateblog')
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True, related_name='rate_blog',
                             related_query_name='rate_blog')


class CommentBlog(models.Model):
    comment = models.TextField()
    photo = models.FileField(upload_to='static/upload/comment/%Y/%m', null=True)
    created_date = models.DateField(null=True, auto_now_add=True)
    updated_date = models.DateField(null=True, auto_now=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='my_user_comment_blog',
                             related_query_name='my_user_comment_blog')
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True, related_name='comment_blog',
                             related_query_name='comment_blog')

    def __str__(self):
        return self.comment


class ReplyBlog(models.Model):
    comment = models.TextField()
    photo = models.FileField(upload_to='static/upload/comment/%Y/%m', null=True)
    created_date = models.DateField(null=True, auto_now_add=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='my_user_reply_blog',
                             related_query_name='my_user_reply_blog')
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True, related_name='reply_blog',
                             related_query_name='reply_blog')
    comment_blog = models.ForeignKey(CommentBlog, on_delete=models.CASCADE,
                                     related_name='comment_reply_blog')