# Generated by Django 4.0.4 on 2022-05-08 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
