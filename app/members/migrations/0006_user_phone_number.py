# Generated by Django 2.1.4 on 2018-12-14 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_user_password2'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
