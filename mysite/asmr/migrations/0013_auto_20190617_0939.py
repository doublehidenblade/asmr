# Generated by Django 2.2.2 on 2019-06-17 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmr', '0012_auto_20190617_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
    ]
