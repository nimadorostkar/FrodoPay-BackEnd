# Generated by Django 4.0.4 on 2022-04-27 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=5, max_digits=30)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='transactions.transaction')),
            ],
            options={
                'verbose_name': 'Transaction fee',
                'verbose_name_plural': 'Transactions fee',
            },
        ),
    ]
