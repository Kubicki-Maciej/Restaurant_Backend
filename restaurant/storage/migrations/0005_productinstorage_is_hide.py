# Generated by Django 4.2 on 2024-01-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_rename_product_productminimal_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinstorage',
            name='is_hide',
            field=models.BooleanField(default=False),
        ),
    ]
