# Generated by Django 4.2 on 2023-07-28 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('product_type', models.CharField(choices=[('KG', 'Kilograms'), ('P', 'Piece')], max_length=20)),
                ('product_EAN', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('name', 'product_type')},
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('storage_EAN', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_date_added', models.DateTimeField(auto_now_add=True)),
                ('product_date_expired', models.DateField()),
                ('number_of_product', models.DecimalField(decimal_places=3, default=0.0, max_digits=10)),
                ('product_waste', models.BooleanField(default=False)),
                ('product_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.product')),
                ('storage_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.storage')),
            ],
        ),
    ]
