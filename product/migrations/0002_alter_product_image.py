# Generated by Django 4.0.6 on 2022-08-04 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='products/image/%Y/%M/'),
        ),
    ]
