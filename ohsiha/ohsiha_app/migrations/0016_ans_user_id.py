# Generated by Django 2.2 on 2020-04-25 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ohsiha_app', '0015_auto_20200425_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='ans',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
