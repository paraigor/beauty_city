# Generated by Django 5.1.4 on 2025-01-12 13:30

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU', unique=True, verbose_name='Телефон')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Админ')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Сотрудник')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Суперпользователь')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('specialty', models.CharField(max_length=200, verbose_name='Специальность')),
                ('photo', models.FileField(blank=True, null=True, upload_to='', verbose_name='Фото мастера')),
            ],
            options={
                'verbose_name': 'Мастер',
                'verbose_name_plural': 'Мастера',
            },
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название салона')),
                ('address', models.TextField(max_length=200, verbose_name='Адрес салона')),
                ('photo', models.FileField(blank=True, null=True, upload_to='', verbose_name='Фото салона')),
            ],
            options={
                'verbose_name': 'Салон',
                'verbose_name_plural': 'Салоны',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название услуги')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена услуги')),
                ('duration', models.PositiveSmallIntegerField(verbose_name='Длительность услуги, мин')),
                ('photo', models.FileField(blank=True, null=True, upload_to='', verbose_name='Фото услуги')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Вид услуги')),
            ],
            options={
                'verbose_name': 'Вид услуги',
                'verbose_name_plural': 'Виды услуг',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата посещения салона')),
                ('comment', models.TextField(verbose_name='Текст отзыва')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='feedbacks', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('not_paid', 'Неоплачено'), ('paid', 'Оплачено')], max_length=20, verbose_name='Статус счета')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Счёт выставлен')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Счёт обновлен')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Счет',
                'verbose_name_plural': 'Счета',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('accepted', 'Принята'), ('ended', 'Завершена'), ('discard', 'Отменена')], max_length=20, verbose_name='Статус записи')),
                ('date', models.DateField(verbose_name='Дата записи')),
                ('start_at', models.TimeField(verbose_name='Время начала')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('invoice', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='beauty_city_app.invoice', verbose_name='Счет')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='beauty_city_app.master', verbose_name='Мастер')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='beauty_city_app.salon', verbose_name='Салон')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='beauty_city_app.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
        migrations.CreateModel(
            name='MasterDaySchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workday', models.DateField(verbose_name='Дата')),
                ('shift_start', models.TimeField(verbose_name='Время начала смены')),
                ('shift_end', models.TimeField(verbose_name='Время окончания смены')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedules', to='beauty_city_app.master', verbose_name='Мастер')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedules', to='beauty_city_app.salon', verbose_name='Салон')),
                ('services', models.ManyToManyField(related_name='schedules', to='beauty_city_app.service', verbose_name='Услуги')),
            ],
            options={
                'verbose_name': 'Расписание мастера',
                'verbose_name_plural': 'Расписания мастеров',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='services', to='beauty_city_app.servicetype', verbose_name='Вид услуги'),
        ),
    ]
