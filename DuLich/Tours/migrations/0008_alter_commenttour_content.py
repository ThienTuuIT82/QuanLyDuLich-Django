# Generated by Django 3.2.5 on 2021-09-19 13:23

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tours', '0007_auto_20210919_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commenttour',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
