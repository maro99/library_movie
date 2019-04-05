# Generated by Django 2.1.7 on 2019-04-04 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_auto_20190405_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='movie',
            field=models.ManyToManyField(through='members.MovieLike', to='movies.Movie'),
        ),
    ]