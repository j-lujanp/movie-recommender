# Generated by Django 3.2.7 on 2021-09-10 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0003_auto_20210909_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='recommender.movie'),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('rating', models.IntegerField(default=0)),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.rater')),
            ],
        ),
    ]