# Generated by Django 2.1 on 2018-08-20 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='historical_answer',
            fields=[
                ('date_id', models.IntegerField(primary_key=True, serialize=False)),
                ('answer', models.TextField()),
                ('name', models.TextField()),
            ],
        ),
    ]