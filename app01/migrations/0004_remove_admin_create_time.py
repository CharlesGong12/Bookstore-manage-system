# Generated by Django 3.2 on 2023-05-04 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='create_time',
        ),
    ]
