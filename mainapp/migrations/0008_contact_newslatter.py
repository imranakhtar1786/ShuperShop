# Generated by Django 4.2.6 on 2023-11-14 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0007_rename_subcategory_checkout_subtotal"),
    ]

    operations = [
        migrations.CreateModel(
            name="contact",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=50)),
                ("phone", models.CharField(max_length=15)),
                ("subject", models.TextField()),
                ("message", models.TextField()),
                ("status", models.BooleanField(default=True)),
                ("date", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="NewsLatter",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]