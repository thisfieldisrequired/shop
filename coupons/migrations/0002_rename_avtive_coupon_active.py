# Generated by Django 4.2.2 on 2023-06-29 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='avtive',
            new_name='active',
        ),
    ]