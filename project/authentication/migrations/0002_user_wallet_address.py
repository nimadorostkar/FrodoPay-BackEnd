# Generated by Django 4.0.4 on 2022-04-21 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wallet_address',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
