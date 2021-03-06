# Generated by Django 2.2 on 2020-04-19 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ohsiha_app', '0006_delete_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respondent_name', models.CharField(max_length=200)),
                ('choise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ohsiha_app.Choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ohsiha_app.Question')),
            ],
        ),
    ]
