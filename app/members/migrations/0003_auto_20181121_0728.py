# Generated by Django 2.1.3 on 2018-11-21 07:28

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_user_img_profile'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', members.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
