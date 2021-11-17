# Generated by Django 3.2.6 on 2021-11-09 09:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0005_auto_20211026_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]
