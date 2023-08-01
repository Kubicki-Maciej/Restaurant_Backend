# Generated by Django 4.2 on 2023-07-31 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20230731_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('none', 'none'), ('waiters', 'waiters'), ('kitchen', 'kitchen'), ('manager', 'manager'), ('owner', 'owner')], default='none', max_length=100),
        ),
    ]