# Generated by Django 3.2.13 on 2022-07-12 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_notiflists'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notiflists',
            name='type',
            field=models.CharField(choices=[('TRANSFER', 'TRANSFER'), ('DEPOSIT', 'DEPOSIT'), ('WITHDRAWAL', 'WITHDRAWAL'), ('USER', 'USER'), ('DEFAULT', 'DEFAULT')], default='DEFAULT', max_length=256),
        ),
    ]
