# Generated by Django 3.0.7 on 2020-06-22 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200622_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articles',
            old_name='userID',
            new_name='user',
        ),
    ]
