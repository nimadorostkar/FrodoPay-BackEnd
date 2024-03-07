# Generated by Django 3.2.13 on 2022-09-19 12:18

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=256, unique=True)),
                ('shop', models.CharField(blank=True, max_length=256, null=True)),
                ('birthday', models.DateField(blank=True, max_length=256, null=True)),
                ('photo', models.ImageField(blank=True, default='user/photo/default.png', null=True, upload_to='user/photo')),
                ('gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female'), ('unspecified', 'unspecified')], default='unspecified', max_length=256, null=True)),
                ('referral', models.CharField(blank=True, max_length=256, null=True)),
                ('wallet_address', models.CharField(blank=True, max_length=256, null=True)),
                ('conf_code', models.IntegerField(blank=True, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('inventory', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('invitation_referral', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefg1234', editable=False, length=8, max_length=15, prefix='')),
                ('invited_users', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('abbreviation', models.CharField(blank=True, max_length=256, null=True, unique=True)),
                ('flag', models.ImageField(default='countries/flag/unknown.png', upload_to='countries/flag')),
            ],
        ),
        migrations.CreateModel(
            name='NotifLists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('body', models.CharField(blank=True, max_length=256, null=True)),
                ('type', models.CharField(choices=[('TRANSFER', 'TRANSFER'), ('DEPOSIT', 'DEPOSIT'), ('WITHDRAWAL', 'WITHDRAWAL'), ('USER', 'USER'), ('DEFAULT', 'DEFAULT')], default='DEFAULT', max_length=256)),
                ('time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.countries'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]