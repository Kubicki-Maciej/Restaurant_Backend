# Generated by Django 4.2 on 2023-07-31 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kitchenorder',
            options={'permissions': [('codename', 'kitchenorder')]},
        ),
    ]
