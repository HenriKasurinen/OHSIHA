# Generated by Django 2.2 on 2020-04-22 15:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ohsiha_app', '0012_auto_20200422_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalkoronadata',
            name='pull_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]