# Generated by Django 4.2.3 on 2023-07-25 18:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('description', models.CharField(max_length=200)),
                ('locked', models.BooleanField(default=False)),
                ('owner', models.CharField(max_length=100)),
                ('lock_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
