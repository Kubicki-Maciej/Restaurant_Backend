# Generated by Django 4.2 on 2023-12-07 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_alter_productinstorage_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductMinimal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_quantity', models.DecimalField(decimal_places=3, default=0.0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.product')),
            ],
        ),
    ]
