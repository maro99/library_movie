# Generated by Django 2.1.3 on 2018-11-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_remove_user_password2'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]