# Generated by Django 3.1.7 on 2021-03-23 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_platform', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
        migrations.AlterField(
            model_name='offer',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.DeleteModel(
            name='Price',
        ),
    ]
