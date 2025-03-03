# Generated by Django 5.1.6 on 2025-03-03 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airtalesapp", "0005_user_groups_user_is_superuser_user_last_login_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="user",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
    ]
