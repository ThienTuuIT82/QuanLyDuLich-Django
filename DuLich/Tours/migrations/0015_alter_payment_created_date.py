# Generated by Django 3.2.5 on 2021-12-22 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tours', '0014_remove_payment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='created_date',
            field=models.DateField(auto_created=True, null=True),
        ),
    ]
