# Generated by Django 4.2 on 2023-07-31 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productinstorage',
            options={'permissions': [('codename', 'productinstorage')]},
        ),
    ]
