# Generated by Django 4.2 on 2023-07-28 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_id', models.IntegerField(blank=True, null=True)),
                ('order_number', models.CharField(max_length=100, null=True)),
                ('ean_code', models.IntegerField(blank=True)),
                ('ean_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('generated_code', models.CharField(max_length=100, null=True)),
                ('order_start', models.DateTimeField(auto_now_add=True)),
                ('order_ends', models.DateTimeField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('cash', 'cash'), ('subscriber', 'subscriber'), ('moderator', 'moderator')], default='cash', max_length=20)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedMeals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_meals', models.IntegerField()),
                ('comments', models.TextField()),
                ('discount', models.CharField(blank=True, choices=[('0', '0'), ('20', '20'), ('30', '30')], max_length=20)),
                ('meal_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]