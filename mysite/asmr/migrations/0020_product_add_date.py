# Generated by Django 2.2.2 on 2019-06-26 10:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('asmr', '0019_auto_20190625_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='add_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期'),
        ),
    ]