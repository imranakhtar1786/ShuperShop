# Generated by Django 4.2.6 on 2023-11-16 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0010_alter_buyer_otp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buyer",
            name="pin",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]