# Generated by Django 4.2.6 on 2023-10-29 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
                ("pic", models.ImageField(upload_to="upload/brand")),
            ],
        ),
        migrations.CreateModel(
            name="Maincategory",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Subcategory",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30)),
                ("baseprice", models.IntegerField()),
                ("discount", models.IntegerField()),
                ("finalprice", models.IntegerField()),
                ("stock", models.BooleanField(default=True)),
                ("color", models.CharField(max_length=30)),
                ("size", models.CharField(max_length=10)),
                ("description", models.TextField(default="")),
                ("pic1", models.ImageField(upload_to="upload/brand")),
                (
                    "pic2",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="upload/brand"
                    ),
                ),
                (
                    "pic3",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="upload/brand"
                    ),
                ),
                (
                    "pic4",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="upload/brand"
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mainapp.brand"
                    ),
                ),
                (
                    "maincategory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mainapp.maincategory",
                    ),
                ),
                (
                    "subcategory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mainapp.subcategory",
                    ),
                ),
            ],
        ),
    ]