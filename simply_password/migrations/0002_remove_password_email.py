# Generated by Django 3.2.7 on 2021-12-12 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simply_password', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='password',
            name='email',
        ),
    ]
