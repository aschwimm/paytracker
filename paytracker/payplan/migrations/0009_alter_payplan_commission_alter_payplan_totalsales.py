# Generated by Django 4.2.5 on 2023-12-19 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payplan', '0008_remove_payplan_flat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payplan',
            name='commission',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='payplan',
            name='totalsales',
            field=models.IntegerField(default=0),
        ),
    ]
