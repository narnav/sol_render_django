# Generated by Django 4.2.3 on 2023-08-23 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_expenses_delete_product'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Trips',
        ),
        migrations.RenameField(
            model_name='expenses',
            old_name='category',
            new_name='Trips',
        ),
    ]