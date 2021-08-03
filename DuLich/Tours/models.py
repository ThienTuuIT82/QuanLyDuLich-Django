from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class Account(AbstractUser):
    avatar = models.ImageField(upload_to='upload/%Y/%m', default=None)


class Category(models.Model):
    class Meta:
        unique_together = ('name',)

    name = models.CharField(max_length=100, null=False, unique=True)


class Tours(models.Model):
    class Meta:
        unique_together = ('name',)
    name = models.CharField(max_length=100, null=False, unique=True)
    description = RichTextField()
    start_date = models.DateTimeField(null=False)
    finish_date = models.DateTimeField(null=False)
    destination = models.CharField(max_length=255,null=False)
    photos = models.ImageField(upload_to='tours/%Y/%m', default=None)
    price = models.CharField(max_length=100, null=False)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category', related_query_name='my_category')
