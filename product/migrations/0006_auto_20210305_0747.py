# Generated by Django 3.1 on 2021-03-05 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='product',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='user',
        ),
    ]
