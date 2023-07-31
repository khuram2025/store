# Generated by Django 3.2.16 on 2023-07-30 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 999.99.'}}, help_text='Maximum 999.99', max_digits=11, verbose_name='Discount price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='regular_price',
            field=models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 999.99.'}}, help_text='Maximum 999.99', max_digits=11, verbose_name='Regular price'),
        ),
    ]