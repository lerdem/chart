# Generated by Django 2.1.2 on 2018-10-31 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20181031_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='randomdata',
            name='date',
            field=models.DateField(),
        ),
    ]