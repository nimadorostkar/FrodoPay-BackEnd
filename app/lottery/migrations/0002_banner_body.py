# Generated by Django 3.2.13 on 2022-07-23 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]