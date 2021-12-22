# Generated by Django 3.2.5 on 2021-12-20 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tours', '0009_auto_20211220_2144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replytour',
            name='comment_tour',
        ),
        migrations.RemoveField(
            model_name='replytour',
            name='tour',
        ),
        migrations.RemoveField(
            model_name='replytour',
            name='user',
        ),
        migrations.AlterField(
            model_name='rateblog',
            name='rate',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ReplyBlog',
        ),
        migrations.DeleteModel(
            name='ReplyTour',
        ),
    ]