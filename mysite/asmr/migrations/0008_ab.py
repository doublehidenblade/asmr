# Generated by Django 2.2.2 on 2019-06-17 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmr', '0007_auto_20190617_0303'),
    ]

    operations = [
        migrations.CreateModel(
            name='ab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, default='', max_length=196)),
                ('password', models.TextField(default='', max_length=30)),
            ],
        ),
    ]
