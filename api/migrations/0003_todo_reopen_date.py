# Generated by Django 2.1.4 on 2022-11-02 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20221102_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='reopen_date',
            field=models.DateTimeField(null=True),
        ),
    ]
