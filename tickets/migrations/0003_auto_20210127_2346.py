# Generated by Django 3.1.4 on 2021-01-27 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_auto_20210124_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organiser',
            field=models.BooleanField(default=True),
        ),
    ]
