# Generated by Django 2.2.2 on 2019-06-14 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmr', '0003_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('order_uid', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]