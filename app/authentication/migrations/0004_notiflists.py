# Generated by Django 3.2.13 on 2022-07-11 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_conf_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifLists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('body', models.CharField(blank=True, max_length=256, null=True)),
                ('type', models.CharField(blank=True, max_length=256, null=True)),
                ('time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]