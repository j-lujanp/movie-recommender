# Generated by Django 3.2.7 on 2021-09-10 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0004_auto_20210910_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='rater',
        ),
    ]
