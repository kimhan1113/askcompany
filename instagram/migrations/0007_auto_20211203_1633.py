# Generated by Django 3.2.6 on 2021-12-03 07:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0006_alter_post_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='as_1',
            field=models.BooleanField(default=False, verbose_name='as_1'),
        ),
        migrations.AddField(
            model_name='post',
            name='as_2',
            field=models.BooleanField(default=False, verbose_name='as_2'),
        ),
        migrations.AddField(
            model_name='post',
            name='as_3',
            field=models.BooleanField(default=False, verbose_name='as_3'),
        ),
        migrations.AddField(
            model_name='post',
            name='car_number',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='post',
            name='fran_name',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_public',
            field=models.BooleanField(blank=True, default=False, verbose_name='공개여부'),
        ),
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(5)]),
        ),
    ]
