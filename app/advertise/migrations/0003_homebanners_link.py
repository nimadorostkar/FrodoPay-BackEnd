# Generated by Django 3.2.13 on 2022-08-09 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0002_homebanners'),
    ]

    operations = [
        migrations.AddField(
            model_name='homebanners',
            name='link',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]