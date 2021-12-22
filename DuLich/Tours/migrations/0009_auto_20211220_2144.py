# Generated by Django 3.2.5 on 2021-12-20 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tours', '0008_auto_20211220_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('children', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='tours',
            name='price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='price_detail', related_query_name='my_price_detail', to='Tours.pricedetail'),
        ),
    ]