# Generated by Django 3.1.7 on 2021-05-20 08:38

import datetime
from django.db import migrations, models


def change_name_len(apps, schema_editor):
    WorkShift = apps.get_model("trade_platform", "WorkShift")
    for workshift in WorkShift.objects.all():
        workshift.name = workshift.name[:16]
        workshift.save()

class Migration(migrations.Migration):

    dependencies = [
        ('trade_platform', '0016_auto_20210520_0826'),
    ]

    operations = [
        migrations.RunPython(change_name_len),
        migrations.AlterField(
            model_name='position',
            name='contract_end_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 8, 38, 41, 372593)),
        ),
        migrations.AlterField(
            model_name='position',
            name='contract_start_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 8, 38, 41, 372579)),
        ),
        migrations.AlterField(
            model_name='workshift',
            name='endtime',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 20, 8, 38, 41, 372138)),
        ),
        migrations.AlterField(
            model_name='workshift',
            name='name',
            field=models.CharField(max_length=16),
        ),
    ]