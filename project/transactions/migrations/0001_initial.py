# Generated by Django 4.0.4 on 2022-05-11 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=254, null=True)),
                ('destination', models.CharField(blank=True, max_length=254, null=True)),
                ('amount', models.DecimalField(decimal_places=5, max_digits=30)),
                ('type', models.CharField(choices=[('deposit', 'deposit'), ('transfer', 'transfer'), ('withdrawal', 'withdrawal')], max_length=254)),
                ('status', models.CharField(choices=[('success', 'success'), ('fail', 'fail')], max_length=254)),
                ('description', models.CharField(blank=True, max_length=254, null=True)),
                ('fee', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
