# Generated by Django 2.2 on 2020-04-23 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ohsiha_app', '0013_auto_20200422_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalkoronadata',
            name='conf_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='externalkoronadata',
            name='reco_amount',
            field=models.IntegerField(default=0),
        ),
    ]
