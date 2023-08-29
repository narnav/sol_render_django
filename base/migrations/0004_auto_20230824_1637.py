# Generated by Django 3.2.20 on 2023-08-24 13:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_category_trips_rename_category_expenses_trips'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency', models.CharField(max_length=3)),
                ('target_currency', models.CharField(max_length=3)),
                ('exchange_rate', models.DecimalField(decimal_places=4, max_digits=10)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='trips',
            name='createdTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='createdTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
