# Generated by Django 3.0.2 on 2020-01-18 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expensive', '0002_auto_20180121_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
