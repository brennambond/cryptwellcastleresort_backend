# Generated by Django 5.1.3 on 2024-12-12 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0002_remove_user_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
