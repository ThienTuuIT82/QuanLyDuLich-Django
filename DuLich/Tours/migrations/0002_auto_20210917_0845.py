# Generated by Django 3.2.5 on 2021-09-17 01:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tours', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commenttour',
            name='updated_date',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='commenttour',
            name='tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Tours.tours'),
        ),
        migrations.AlterField(
            model_name='commenttour',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
