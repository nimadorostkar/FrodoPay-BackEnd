# Generated by Django 4.0.4 on 2022-04-21 08:54

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_alter_wallet_wallet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefg1234', editable=False, length=22, max_length=40, prefix='', unique=True),
        ),
    ]
