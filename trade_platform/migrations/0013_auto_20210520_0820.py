# Generated by Django 3.1.7 on 2021-05-20 08:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_platform', '0012_auto_20210520_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='contract_end_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 8, 20, 37, 320683)),
        ),
        migrations.AlterField(
            model_name='position',
            name='contract_start_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 8, 20, 37, 320670)),
        ),
        migrations.AlterField(
            model_name='workshift',
            name='endtime',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 20, 8, 20, 37, 320249)),
        ),
        migrations.AlterField(
            model_name='workshift',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 20, 8, 20, 37, 320234)),
        ),
    ]
