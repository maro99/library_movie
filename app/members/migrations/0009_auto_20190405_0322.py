# Generated by Django 2.1.7 on 2019-04-04 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20190319_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='movie',
            field=models.ManyToManyField(blank=True, through='members.MovieLike', to='movies.Movie'),
        ),
    ]
