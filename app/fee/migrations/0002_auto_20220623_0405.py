# Generated by Django 3.2.13 on 2022-06-23 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feerates',
            name='deposit',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=30),
        ),
        migrations.AlterField(
            model_name='feerates',
            name='transfer',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=30),
        ),
        migrations.AlterField(
            model_name='feerates',
            name='withdrawal',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=30),
        ),
    ]