# Generated by Django 5.1.7 on 2025-03-24 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_alter_category_description_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.BigIntegerField(default=100000000),
            preserve_default=False,
        ),
    ]
