# Generated by Django 4.2.7 on 2025-01-09 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0005_moodentry_local_timezone_alter_moodentry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moodentry',
            name='date',
            field=models.DateTimeField(),
        ),
    ]