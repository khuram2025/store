# Generated by Django 4.2.2 on 2023-06-25 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_productspecificationvalue_value_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productspecificationvalue',
            name='boolean_value',
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='type',
            field=models.CharField(choices=[('text', 'Text Field'), ('choices', 'Dropdown List')], default='text', max_length=10),
        ),
    ]