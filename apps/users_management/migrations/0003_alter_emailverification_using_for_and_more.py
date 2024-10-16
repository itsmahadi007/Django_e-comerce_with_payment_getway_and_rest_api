# Generated by Django 4.2 on 2024-10-11 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users_management", "0002_phoneverification_emailverification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailverification",
            name="using_for",
            field=models.CharField(
                choices=[
                    ("email_verification", "Email Verification"),
                    ("password_reset", "Password Reset"),
                    ("no_request", "No Request"),
                ],
                default="no_request",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="phoneverification",
            name="using_for",
            field=models.CharField(
                choices=[
                    ("email_verification", "Email Verification"),
                    ("password_reset", "Password Reset"),
                    ("no_request", "No Request"),
                ],
                default="no_request",
                max_length=100,
            ),
        ),
    ]
