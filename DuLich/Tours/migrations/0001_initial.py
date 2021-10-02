# Generated by Django 3.2.5 on 2021-09-08 10:01

import ckeditor.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('photo', models.FileField(null=True, upload_to='static/upload/blog/%Y/%m')),
                ('created_date', models.DateField(null=True)),
                ('description', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='CommentBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('photo', models.FileField(null=True, upload_to='static/upload/comment/%Y/%m')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_blog', related_query_name='comment_blog', to='Tours.blog')),
            ],
        ),
        migrations.CreateModel(
            name='CommentTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('photo', models.FileField(null=True, upload_to='static/upload/comment/%Y/%m')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(choices=[('MALE', 'Nam'), ('FEMALE', 'Nữ')], default='Nam', max_length=20, null=True)),
                ('birth', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('BUSINESS', 'Nhân viên kinh doanh'), ('SALESMAN', 'Nhân viên bán hàng'), ('EMPLOYEE_MANAGER', 'Quản lý nhân sự'), ('MANAGER', 'Quản lý'), ('USER', 'Khách hàng')], default='Khách hàng', max_length=20)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='static/upload/avatars/%Y/%m')),
                ('street', models.CharField(blank=True, max_length=45, null=True)),
                ('about', models.CharField(blank=True, max_length=45, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='province', related_query_name='province', to='Tours.province')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('destination', models.CharField(max_length=255)),
                ('photos', models.ImageField(default=None, upload_to='static/upload/tours/%Y/%m')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vehicle', models.CharField(choices=[('OTO', 'Ô tô'), ('YACHT', 'Du thuyền'), ('PLANE', 'Máy bay')], max_length=20, null=True)),
                ('active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', related_query_name='my_category', to='Tours.category')),
                ('tags', models.ManyToManyField(related_name='tags', related_query_name='my_tags', to='Tours.Tag')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_tour', related_query_name='user_tour', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='TourBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('CANCELLED', 'Cancelled'), ('ARCHIVED', 'Archived')], default='Active', max_length=20, null=True)),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tourbooking_payment', related_query_name='tourbooking_payment', to='Tours.tours')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_tourbooking', related_query_name='user_tourbooking', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('photo', models.FileField(null=True, upload_to='static/upload/comment/%Y/%m')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('comment_tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_reply_tour', to='Tours.commenttour')),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reply_payment', related_query_name='reply_payment', to='Tours.tours')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_user_reply_tour', related_query_name='my_user_reply_tour', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('photo', models.FileField(null=True, upload_to='static/upload/comment/%Y/%m')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reply_blog', related_query_name='reply_blog', to='Tours.blog')),
                ('comment_blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_reply_blog', to='Tours.commentblog')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_user_reply_blog', related_query_name='my_user_reply_blog', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RateTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.CharField(choices=[('LIKE', 'Like'), ('DISLIKE', 'Dislike')], max_length=20)),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rate_payment', related_query_name='rate_payment', to='Tours.tours')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_user_ratetour', related_query_name='my_user_ratetour', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RateBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.CharField(choices=[('LIKE', 'Like'), ('DISLIKE', 'Dislike')], max_length=20)),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rate_blog', related_query_name='rate_blog', to='Tours.blog')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_user_rateblog', related_query_name='my_user_rateblog', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_created=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('method', models.CharField(choices=[('ZALOPAY', 'ZaloPay'), ('MOMO', 'Momo'), ('TRANSFER', 'Chuyển khoản')], default='Chuyển khoản', max_length=20, null=True)),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tour_payment', related_query_name='tour_payment', to='Tours.tours')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_payment', related_query_name='user_payment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='commenttour',
            name='tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_payment', related_query_name='comment_payment', to='Tours.tours'),
        ),
        migrations.AddField(
            model_name='commenttour',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_user_comment_tour', related_query_name='my_user_comment_tour', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentblog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_user_comment_blog', related_query_name='my_user_comment_blog', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_user_blog', related_query_name='my_user_blog', to=settings.AUTH_USER_MODEL),
        ),
    ]
