# Generated by Django 2.1 on 2018-09-28 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0006_auto_20180924_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='afew_experiment_session',
            name='time_stamp',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
