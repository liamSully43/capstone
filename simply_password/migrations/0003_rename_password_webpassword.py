# Generated by Django 3.2.7 on 2021-12-12 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simply_password', '0002_remove_password_email'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Password',
            new_name='WebPassword',
        ),
    ]
