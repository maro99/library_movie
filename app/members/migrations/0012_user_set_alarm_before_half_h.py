# Generated by Django 2.2.1 on 2019-06-10 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20190406_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='set_alarm_before_half_h',
            field=models.BooleanField(default=False),
        ),
    ]
