# Generated by Django 4.2.5 on 2023-12-24 06:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payplan', '0015_rename_sales_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='datelogged',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
