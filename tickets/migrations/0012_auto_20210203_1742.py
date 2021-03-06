# Generated by Django 3.1.4 on 2021-02-03 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0011_auto_20210203_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_official',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='category',
            field=models.CharField(choices=[('Finance', 'Finance'), ('IT', 'IT'), ('Procurement', 'Procurement')], max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_organiser',
            field=models.BooleanField(default=False),
        ),
    ]
