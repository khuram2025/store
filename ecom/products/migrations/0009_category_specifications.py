# Generated by Django 3.2.16 on 2023-08-08 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20230730_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='specifications',
            field=models.ManyToManyField(blank=True, to='products.ProductSpecification'),
        ),
    ]