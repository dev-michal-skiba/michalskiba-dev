# Generated by Django 4.2.3 on 2023-10-04 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("demo", "0002_populate_users"),
        ("web_parameter_tampering", "0005_delete_all_press_applications"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pressapplication",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="press_application",
                to="demo.demouser",
            ),
        ),
    ]