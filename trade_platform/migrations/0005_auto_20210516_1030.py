# Generated by Django 3.1.7 on 2021-05-16 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade_platform', '0004_auto_20210325_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkShift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='inventory',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_inventory', to='trade_platform.item'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_inventory', to='trade_platform.profile'),
        ),
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_currency', to='trade_platform.currency'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_item', to='trade_platform.item'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_person', to='trade_platform.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currency', to='trade_platform.currency'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_trade', to='trade_platform.item'),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('workshifts', models.ManyToManyField(related_name='positions', to='trade_platform.WorkShift')),
            ],
        ),
    ]